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
    assert len(deps) == 2
    current_version = {}
    for i, pkg in enumerate(["formattex", "formatbibtex"]):
        formattex_dep = Requirement(deps[i])
        assert formattex_dep.name == pkg
        formattex_specs = list(formattex_dep.specifier)
        assert len(formattex_specs) == 1
        assert formattex_specs[0].operator == "=="
        current_version[pkg] = Version(formattex_specs[0].version)

    print("Current versions:", current_version)

    pkg_versions = {}

    for pkg in "formattex", "formatbibtex":
        # get all versions of <pkg> from PyPI
        resp = urllib3.request("GET", f"https://pypi.org/pypi/{pkg}/json")
        if resp.status != 200:
            raise RuntimeError

        versions = [Version(release) for release in resp.json()["releases"]]
        versions = [
            v for v in versions if v > current_version[pkg] and not v.is_prerelease
        ]
        versions.sort()
        pkg_versions[pkg] = versions

    print("New versions:", pkg_versions)

    try:
        formatbibtex_version = pkg_versions["formatbibtex"][-1]
    except IndexError:
        formatbibtex_version = current_version["formatbibtex"]

    for version in pkg_versions["formattex"]:
        pyproject["project"]["dependencies"] = [
            f"formattex=={version}",
            f"formatbibtex=={formatbibtex_version}",
        ]
        with open(Path(__file__).parent / "pyproject.toml", "wb") as f:
            print(pyproject)
            tomli_w.dump(pyproject, f)
        # subprocess.run(["git", "add", "pyproject.toml"])
        # subprocess.run(["git", "commit", "-m", f"formattex {version}"])
        # subprocess.run(["git", "tag", f"{version}"])


if __name__ == "__main__":
    main()
