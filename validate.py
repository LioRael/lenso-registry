"""Validate public Registry identities and exact published manifest digests."""
import hashlib
import json
from pathlib import Path
import re
import tomllib
from urllib.request import Request, urlopen


def download(url):
    with urlopen(Request(url, headers={"User-Agent": "lenso-registry-validation"}), timeout=30) as response:
        body = response.read(1024 * 1024 + 1)
    if len(body) > 1024 * 1024:
        raise ValueError("metadata exceeds 1 MiB")
    return body


packages = set()
for path in Path("extensions").glob("*.json"):
    index = json.loads(path.read_text())
    assert index["schema_version"] == 1
    assert index["name"] == "@lenso/" + path.stem
    assert 0 < len(index["releases"]) <= 4096
    packages.add(index["name"])
    versions = set()
    for release in index["releases"]:
        version = release["version"]
        assert re.fullmatch(r"\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?(?:\+[A-Za-z0-9.-]+)?", version)
        assert version not in versions
        versions.add(version)
        assert re.fullmatch(r"[0-9a-f]{64}", release["sha256"])
        match = re.fullmatch(r"github-release:([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/([A-Za-z0-9_-]+)", release["source"])
        assert match
        repo, package = match.groups()
        descriptor = tomllib.loads(download(f"https://raw.githubusercontent.com/{repo}/HEAD/lenso.registry.toml").decode())
        assert descriptor["schema_version"] == 1
        author = next(item for item in descriptor["extensions"] if item["id"] == package)
        tag = author.get("tag", "v{version}").replace("{version}", version).replace("{id}", package)
        assert re.fullmatch(r"[A-Za-z0-9_.-]+", tag)
        metadata = json.loads(download(f"https://github.com/{repo}/releases/download/{tag}/lenso-release.json"))
        assert metadata["schema_version"] == 1 and metadata["id"] == package and metadata["version"] == version
        assert metadata["manifest"]["sha256"] == release["sha256"]
        manifest = download(f"https://github.com/{repo}/releases/download/{tag}/" + metadata["manifest"]["name"])
        assert hashlib.sha256(manifest).hexdigest() == release["sha256"]
        definition = tomllib.loads(manifest.decode())
        assert definition["schema_version"] == 1 and definition["id"] == package and definition["version"] == version
        for handler in definition["handlers"].values():
            if handler["type"] == "wasm":
                assert re.fullmatch(r"[0-9a-f]{64}", handler["sha256"])
for path in Path("presets").glob("*.toml"):
    preset = tomllib.loads(path.read_text())
    assert preset["schema_version"] == 1 and preset["id"] == "@lenso/" + path.stem
    assert preset.get("create") or preset.get("adopt")
    for extension in preset["extensions"]:
        assert extension["source"].removeprefix("registry:") in packages
print("Registry identities, published digests, Wasm pins and preset references passed.")
