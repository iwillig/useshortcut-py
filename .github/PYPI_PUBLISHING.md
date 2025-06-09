# PyPI Publishing with GitHub Actions

This repository has automated PyPI publishing set up through GitHub Actions. Here's how it works:

## Automated Publishing Methods

### 1. **Automatic on Version Change** (`publish.yml`)
When you merge a PR to main that changes the version in `setup.py`:
1. The workflow detects the version change
2. Runs tests to ensure everything works
3. Creates a git tag for the version
4. Publishes to Test PyPI (optional)
5. Publishes to PyPI
6. Creates a GitHub release

**To trigger:**
1. Update version in `setup.py`
2. Commit and push to a branch
3. Create and merge a PR
4. The package will be automatically published when merged

### 2. **Manual Release** (`publish-release.yml`)
Publish by creating a GitHub release:
1. Go to Releases → Create a new release
2. Create a new tag (e.g., `v0.1.0`)
3. Fill in release notes
4. Publish the release
5. The workflow will build and publish to PyPI

**To trigger manually:**
- Go to Actions → "Publish Release" → Run workflow

## Setup Requirements

### 1. PyPI Account Setup
1. Create an account on [PyPI](https://pypi.org)
2. Create an account on [Test PyPI](https://test.pypi.org) (optional)

### 2. Configure Trusted Publishing (Recommended)
Instead of using API tokens, use PyPI's trusted publishing:

1. Go to your PyPI account settings
2. Navigate to "Publishing"
3. Add a new trusted publisher:
   - Owner: `iwillig`
   - Repository: `useshortcut-py`
   - Workflow name: `publish.yml` (or `publish-release.yml`)
   - Environment: `pypi`

### 3. GitHub Repository Settings
1. Go to Settings → Environments
2. Create an environment named `pypi`
3. (Optional) Add protection rules:
   - Required reviewers
   - Restrict to main branch

## Version Management

### Semantic Versioning
Follow semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking API changes
- MINOR: New features (backwards compatible)
- PATCH: Bug fixes

### Version Locations
Update version in these files:
1. `setup.py` - The source of truth
2. `useshortcut/client.py` - User-Agent string (optional)

### Example Version Bump
```bash
# Edit setup.py
version="0.1.0"  # Changed from 0.0.1

# Commit
git add setup.py
git commit -m "Bump version to 0.1.0"

# Push and create PR
git push origin feature/version-bump
```

## Testing Before Publishing

### Local Testing
```bash
# Build locally
pipenv run python -m build

# Check the package
pipenv run twine check dist/*

# Test upload to Test PyPI
pipenv run twine upload --repository testpypi dist/*
```

### Test Installation
```bash
# From Test PyPI
pip install --index-url https://test.pypi.org/simple/ useshortcut

# From PyPI (after publishing)
pip install useshortcut
```

## Troubleshooting

### Publishing Failed
1. Check the Actions tab for error logs
2. Ensure version number was incremented
3. Verify PyPI trusted publishing is configured
4. Check that tests pass locally

### Version Already Exists
- PyPI doesn't allow overwriting versions
- Increment the version number and try again

### Authentication Errors
- Ensure trusted publishing is set up correctly
- Environment name must match: `pypi`
- Workflow filename must match configuration

## Manual Publishing (Fallback)

If automated publishing fails, you can publish manually:

```bash
# Build
pipenv run python -m build

# Upload to Test PyPI
pipenv run twine upload --repository testpypi dist/*

# Upload to PyPI
pipenv run twine upload dist/*
```

## Best Practices

1. **Always test on Test PyPI first** for major changes
2. **Update CHANGELOG.md** before releasing
3. **Create detailed release notes** in GitHub
4. **Tag releases** with `v` prefix (e.g., `v1.0.0`)
5. **Run tests locally** before pushing version changes

## Release Checklist

- [ ] Update version in `setup.py`
- [ ] Update CHANGELOG.md
- [ ] Run tests locally: `pipenv run pytest`
- [ ] Run formatter: `pipenv run black .`
- [ ] Commit changes
- [ ] Create PR with clear description
- [ ] Merge PR (triggers automatic publishing)
- [ ] Verify package on PyPI
- [ ] Announce release (optional)