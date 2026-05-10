# Release Procedure

## 1. Merge all changes to main

Merge all feature branches via pull requests.

## 2. Bump the version

Choose `patch`, `minor`, or `major` according to [Semantic Versioning](https://semver.org/):

| Change | Version bump |
|---|---|
| Bug fixes | `patch` (1.0.1 → 1.0.2) |
| New features, backward-compatible | `minor` (1.0.1 → 1.1.0) |
| Breaking changes | `major` (1.0.1 → 2.0.0) |

```bash
poetry version minor   # or patch / major
git add pyproject.toml
git commit -m "chore: bump version to $(poetry version -s)"
git push origin main
```

## 3. Create a GitHub Release

Go to [Releases → Draft a new release](https://github.com/Hiraoka-Group/nasap-net/releases/new):

- **Tag**: `v1.1.0` (create new tag matching the version in `pyproject.toml`)
- **Target**: `main`
- **Title**: `v1.1.0`
- **Description**: release notes

Publishing the release triggers the CI workflow, which runs tests, builds the package, and publishes to PyPI automatically.
