# Lenso Registry

The official extension and preset catalog consumed by Lenso CLI 0.2 and newer.
GitHub hosts the index; prebuilt executable packages live in authors' GitHub Releases.
Consumers require neither Node.js nor Git. The Registry grants no capabilities.

- `extensions/<package>.json`: a namespaced package's immutable versions, GitHub Release sources, and manifest SHA-256 values.
- `presets/<name>.toml`: versioned compositions with package constraints and optional create/adopt recipes.

Official short names resolve as `@lenso/<name>`. A project may configure additional
Registry namespace routes. Business resource catalogs belong to their extensions.

Code 0.3.3 and the Code preset 0.3.3 require Lenso CLI 1.0.0 (Host 0.2.4,
Project 0.1.2). Install through the official names and review the requested setup:

```sh
lenso ext add code                 # Add to an initialized project
lenso new my-app --preset code     # Create a project
lenso init --preset code           # Adopt an existing project
lenso preset apply code            # Apply or refresh the preset selection
```

Code asks for a resource repository, or accepts local author settings through
`--input '{"author_root":"author","target":"src"}'`. Version 0.2.0 adds
composition, template validation and generation, incremental updates, adapter
cleanup and reviewed Cargo/npm dependency plans. See the
[Code author guide](https://github.com/LioRael/lenso-cli/blob/main/docs/code-generation.md).
Functional modules belong to Code, rather than extension presets:

```sh
lenso init --preset code
lenso code search auth
lenso code preview auth
lenso code add auth
```

Code resolves its own module directory, language/runtime choices, adapter bindings,
source versions and generation plans. The Host Registry only resolves extensions
and presets. The historical Auth preset remains available for existing installs,
but is omitted from preset discovery. SDK code is unchanged.

Code 0.3.3 reads project conventions and defaults from root `lenso.code.toml`.
Use `lenso code config` to inspect settings or review changes through flags:

```sh
lenso code config --language typescript --runtime node26
lenso code config --modules-path src/modules --import-alias '@/modules'
lenso code config --provider lenso.auth-store=postgres
lenso code preview auth
lenso code add auth
```

Directory target `when` conditions select fixed implementations; capability slots
remain flexible adapter choices. Missing conventions are asked before generation
and saved only after approval. Existing module choices win over project defaults.
Changing installed conventions requires `--reconfigure`; language/runtime changes
require another project target. See the
[project configuration guide](https://github.com/LioRael/lenso-cli/blob/main/docs/code-project-configuration.md).

To upgrade an initialized project, use `lenso ext add code --constraint '^0.3.3'`
and review setup access to the new config file. Use `lenso preset apply code` to
refresh its preset selection. SDK code remains unchanged.

Existing project locks retain their pinned versions until explicitly refreshed;
older immutable package records remain available.

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
