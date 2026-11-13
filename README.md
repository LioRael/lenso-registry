# Lenso Registry

The official extension and preset catalog consumed by Lenso CLI 0.2 and newer.
GitHub hosts the index; prebuilt executable packages live in authors' GitHub Releases.
Consumers require neither Node.js nor Git. The Registry grants no capabilities.

- `extensions/<package>.json`: a namespaced package's immutable versions, GitHub Release sources, and manifest SHA-256 values.
- `presets/<name>.toml`: versioned compositions with package constraints and optional create/adopt recipes.

Official short names resolve as `@lenso/<name>`. A project may configure additional
Registry namespace routes. Business resource catalogs belong to their extensions.

Code 0.3.1 and the Code preset 0.3.1 require Lenso CLI 1.0.0 (Host 0.2.4,
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
Auth 0.2.0 is available through `lenso init --preset auth` in a prepared native
application. Choose TypeScript/Node.js 26 or Rust/Tokio, then run `lenso code validate`,
`lenso code compose-preview --sample default` and `lenso code compose --sample default`.
Agents can pass `--input '{"language":"rust"}'` during initialization. The preset
uses pinned [module sources](https://github.com/LioRael/lenso-modules/tree/v0.2.0),
SQLite or PostgreSQL and scrypt; generated dependencies require the selected language toolchain.
It adopts an existing `package.json`/`Cargo.toml` application, rather than creating
a full application scaffold. Language/runtime changes require a new target. PostgreSQL reads `DATABASE_URL` at
application runtime; previews and receipts contain only an environment reference.
Use the `postgres` sample for PostgreSQL or the `default` sample for SQLite.
Store switching reconciles owned source/dependencies after authorization and leaves
existing database data intact; it does not convert data between stores.
Code 0.3 adds these preset defaults and explicit target choices without embedding
business logic in the Host or changing the SDK.

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
