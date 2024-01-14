import subprocess
from pathlib import Path

import tomli
import tomli_w
import urllib3
from packaging.requirements import Requirement
from packaging.version import Version


def main():
    with open(Path(__file__).parent / "pyproject.toml", "rb") as f:
        pyproject = tomli.load(f)

    # get current version of formattex
    deps = pyproject["project"]["dependencies"]
    # TODO: work on update for formatbibtex
    assert len(deps) == 1
    formattex_dep = Requirement(deps[0])
    assert formattex_dep.name == "formattex"
    formattex_specs = list(formattex_dep.specifier)
    assert len(formattex_specs) == 1
    assert formattex_specs[0].operator == "=="
    current_version = Version(formattex_specs[0].version)

    # get all versions of formattex from PyPI
    resp = urllib3.request("GET", "https://pypi.org/pypi/formattex/json")
    if resp.status != 200:
        raise RuntimeError

    versions = [Version(release) for release in resp.json()["releases"]]
    versions = [v for v in versions if v > current_version and not v.is_prerelease]
    versions.sort()

    for version in versions:
        pyproject["project"]["dependencies"] = [f"formattex=={version}"]
        with open(Path(__file__).parent / "pyproject.toml", "wb") as f:
            tomli_w.dump(pyproject, f)
        subprocess.run(["git", "add", "pyproject.toml"])
        subprocess.run(["git", "commit", "-m", f"formattex {version}"])
        subprocess.run(["git", "tag", f"{version}"])


if __name__ == "__main__":
    main()
