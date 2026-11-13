# Lenso Registry

The official extension and preset catalog consumed by Lenso CLI 0.2 and newer.
GitHub hosts the index; prebuilt executable packages live in authors' GitHub Releases.
Consumers require neither Node.js nor Git. The Registry grants no capabilities.

- `extensions/<package>.json`: a namespaced package's immutable versions, GitHub Release sources, and manifest SHA-256 values.
- `presets/<name>.toml`: versioned compositions with package constraints and optional create/adopt recipes.

Official short names resolve as `@lenso/<name>`. A project may configure additional
Registry namespace routes. Business resource catalogs belong to their extensions.

Publish an extension with `lenso publish --github`, then use the author tool in the
CLI repository to propose registration:

```sh
python3 scripts/registry-entry.py --metadata dist/lenso/lenso-release.json \
  --repo owner/extensions --name @lenso/package --submit
```

The tool needs Python and authenticated `gh` on the author's machine; these are not
consumer dependencies. Maintainers may submit directly. Other authors fork this
repository and pass `--head-repo YOUR_ACCOUNT/lenso-registry`. The tool creates a
review branch and PR, never merges it, and never replaces an existing version.
Reviewers check ownership, package behavior and grants in addition to CI integrity
checks. Do not submit credentials or change an existing published version's digest.
