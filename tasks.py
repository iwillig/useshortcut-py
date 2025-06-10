from invoke import task, Context
import sys
import os
import json
import requests


@task
def test(c: Context, verbose: bool = False):
    """Run the test suite"""
    cmd = "pipenv run pytest"
    if verbose:
        cmd += " -v"
    c.run(cmd, pty=True)


@task
def format(c: Context, check: bool = False):
    """Format code with black"""
    cmd = "pipenv run black ."
    if check:
        cmd += " --check"
    c.run(cmd, pty=True)


@task
def lint(c: Context):
    """Run linting checks"""
    print("Running black check...")
    c.run("pipenv run black --check .", pty=True)


@task
def clean(c: Context):
    """Clean up cache and build files"""
    patterns = [
        "**/__pycache__",
        "**/*.pyc",
        ".pytest_cache",
        "*.egg-info",
        "dist",
        "build",
        ".coverage",
        "htmlcov",
    ]

    for pattern in patterns:
        c.run(
            f"find . -type d -name '{pattern}' -exec rm -rf {{}} + 2>/dev/null || true"
        )
        c.run(
            f"find . -type f -name '{pattern}' -exec rm -f {{}} + 2>/dev/null || true"
        )

    print("Cleaned up cache and build files")


@task
def install(c: Context, dev: bool = True):
    """Install dependencies using pipenv"""
    cmd = "pipenv install"
    if dev:
        cmd += " --dev"
    c.run(cmd, pty=True)


@task
def build(c: Context):
    """Build the package"""
    print("Building distribution packages...")
    c.run("pipenv run python -m build", pty=True)
    print("\nBuild complete! Check the dist/ directory for packages.")


@task
def publish(c: Context, test: bool = True):
    """Publish the package to PyPI"""
    if test:
        c.run("twine upload --repository testpypi dist/*", pty=True)
    else:
        c.run("twine upload dist/*", pty=True)


@task(pre=[clean, format, test])
def ci(c: Context):
    """Run all CI checks (clean, format, test)"""
    print("All CI checks passed!")


@task
def demo(c: Context):
    """Run a demo of the client"""
    if not os.environ.get("SHORTCUT_API_TOKEN"):
        print("Error: SHORTCUT_API_TOKEN environment variable not set")
        sys.exit(1)

    c.run("pipenv run python tests/test_client.py", pty=True)


@task
def shell(c: Context):
    """Start an interactive Python shell with the client loaded"""
    c.run(
        "pipenv run python -i -c "
        '"import os; from useshortcut.client import APIClient; '
        "import useshortcut.models as models; "
        'client = APIClient(api_token=os.environ.get(\\"SHORTCUT_API_TOKEN\\")) '
        'if os.environ.get(\\"SHORTCUT_API_TOKEN\\") else None; '
        'print(\\"Loaded: APIClient as client, models\\"); '
        'print(\\"Set SHORTCUT_API_TOKEN to use the client\\")"',
        pty=True,
    )


@task
def docs(c: Context, serve: bool = False):
    """Generate or serve documentation"""
    print("Documentation generation not yet configured")
    print("Consider adding sphinx or mkdocs for documentation")


@task
def coverage(c: Context, html: bool = False):
    """Run tests with coverage"""
    c.run("pipenv run pytest --cov=useshortcut --cov-report=term", pty=True)
    if html:
        c.run("pipenv run pytest --cov=useshortcut --cov-report=html", pty=True)
        print("Coverage report generated in htmlcov/")


@task
def update(c: Context):
    """Update dependencies"""
    c.run("pipenv update", pty=True)


@task
def check(c: Context):
    """Check for dependency updates"""
    c.run("pipenv update --outdated", pty=True)


@task
def fetch_api_docs(c: Context, output: str = "shortcut-api-v3.yaml"):
    """Fetch the OpenAPI documentation from Shortcut API v3

    Args:
        output: Output filename for the API docs (default: shortcut-api-v3.yaml)
    """
    import yaml

    url = "https://api.app.shortcut.com/api/v3/docs"

    response = requests.get(url)
    response.raise_for_status()

    api_docs = response.json()

    with open(output, "w") as f:
        yaml.dump(api_docs, f, default_flow_style=False, sort_keys=False)
