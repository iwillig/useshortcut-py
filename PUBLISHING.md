# Publishing to PyPI

This guide explains how to publish the `useshortcut` package to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on:
   - [PyPI](https://pypi.org/account/register/) - Production
   - [TestPyPI](https://test.pypi.org/account/register/) - Testing

2. **API Tokens**: Generate API tokens for both PyPI and TestPyPI:
   - Go to Account Settings → API tokens
   - Create a token with "Entire account" scope
   - Save these tokens securely

3. **Install Dependencies**:
   ```bash
   pipenv install --dev
   ```

## Pre-Publishing Checklist

- [ ] Update version number in `setup.py`
- [ ] Update CHANGELOG.md (if you have one)
- [ ] Run tests: `pipenv run invoke test`
- [ ] Format code: `pipenv run invoke format`
- [ ] Commit all changes
- [ ] Tag the release: `git tag -a v0.0.1 -m "Version 0.0.1"`

## Building the Package

1. Clean previous builds:
   ```bash
   pipenv run invoke clean
   ```

2. Build the distribution packages:
   ```bash
   pipenv run python -m build
   ```

   This creates:
   - `dist/useshortcut-0.0.1.tar.gz` (source distribution)
   - `dist/useshortcut-0.0.1-py3-none-any.whl` (wheel)

## Testing on TestPyPI

1. Upload to TestPyPI:
   ```bash
   pipenv run twine upload --repository testpypi dist/*
   ```

2. When prompted, use:
   - Username: `__token__`
   - Password: Your TestPyPI API token

3. Test installation:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ --no-deps useshortcut
   ```

4. Verify the package works:
   ```python
   from useshortcut.client import APIClient
   print("Import successful!")
   ```

## Publishing to PyPI

1. Once testing is successful, upload to PyPI:
   ```bash
   pipenv run twine upload dist/*
   ```

2. When prompted, use:
   - Username: `__token__`
   - Password: Your PyPI API token

3. Verify on PyPI: https://pypi.org/project/useshortcut/

## Using .pypirc (Optional)

To avoid entering credentials each time, create `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-TOKEN-HERE

[testpypi]
username = __token__
password = pypi-YOUR-TEST-TOKEN-HERE
```

Set proper permissions:
```bash
chmod 600 ~/.pypirc
```

Then you can upload without entering credentials:
```bash
pipenv run twine upload dist/*
pipenv run twine upload --repository testpypi dist/*
```

## Post-Publishing

1. Install from PyPI to verify:
   ```bash
   pip install useshortcut
   ```

2. Push git tags:
   ```bash
   git push origin --tags
   ```

3. Create a GitHub release (optional)

## Automating with Invoke

Use the provided invoke tasks:

```bash
# Build the package
pipenv run invoke build

# Publish to TestPyPI
pipenv run invoke publish --test

# Publish to PyPI
pipenv run invoke publish --no-test
```

## Version Management

When releasing a new version:

1. Update version in `setup.py`
2. Update version in `useshortcut/client.py` (User-Agent)
3. Commit: `git commit -am "Bump version to X.Y.Z"`
4. Tag: `git tag -a vX.Y.Z -m "Version X.Y.Z"`
5. Build and publish

## Troubleshooting

- **"Invalid distribution file"**: Ensure you're using the latest versions of `build` and `twine`
- **"Package already exists"**: You can't overwrite existing versions; bump the version number
- **Import errors after installation**: Check that all package files are included in MANIFEST.in
- **Authentication failed**: Ensure you're using `__token__` as username and your API token as password

## Best Practices

1. Always test on TestPyPI first
2. Use semantic versioning (MAJOR.MINOR.PATCH)
3. Keep a CHANGELOG.md
4. Write comprehensive release notes
5. Test the installed package in a clean virtual environment