#!/usr/bin/env python3
# **************************************************************************************************************
#
# gen_doc.py
#
# Generates a small Markdown page ('about_this_documentation.md') that states which
# component version the documentation refers to and when the documentation
# itself was generated - information that is otherwise missing from the
# built HTML documentation (e.g. 'appendix/about.html') - and then triggers
# the actual documentation build via 'properdocs build'.
#
# Component-agnostic by design: all paths and the build command are read
# from a JSON configuration file, so the same script can be reused for other
# components just by pointing it to a different configuration file.
#
# JSON configuration file (default name: 'gen_doc_config.json', expected in
# the same folder as this script unless '--config' is given):
#
#   {
#     "version_file":         "<path to the component's version.py, relative to this JSON file>",
#     "output_file":           "<path of the Markdown file to generate, relative to this JSON file>",
#     "history_file":          "<optional: path to history.md, relative to this JSON file; omit or null to disable>",
#     "properdocs_command":    "<command line used to build the documentation (environment variables are expanded)>",
#     "properdocs_cwd":        "<optional: working directory for 'properdocs_command', relative to this JSON file;
#                                 default: the JSON file's own directory>"
#   }
#
# 'version_file' is expected to define two module level string constants, e.g.:
#   VERSION      = "0.13.0"
#   VERSION_DATE = "03.11.2026"
#
# 'history_file', if configured, is expected to contain a Markdown table
# whose first column holds version numbers (one version per table row, e.g.
# '| 0.12.0 | 02.02.2026 | ... |'). If the version found in 'version_file'
# has no matching row, a warning is printed (this does not stop the build).
#
# Aufruf:
#   python gen_doc.py [--config <Pfad zur JSON-Konfigurationsdatei>]
#
# **************************************************************************************************************

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent


def _resolve(base_dir: Path, path_str: str) -> Path:
    """Resolves 'path_str' (as found in the JSON config) relative to
    'base_dir' (the JSON config file's own directory)."""
    return (base_dir / path_str).resolve()


def _load_config(config_file: Path) -> dict:
    """Loads and minimally validates the JSON configuration file."""
    with open(config_file, encoding="utf-8-sig") as fh:
        config = json.load(fh)

    for required_key in ("version_file", "output_file", "properdocs_command"):
        if required_key not in config:
            raise ValueError(f"'{config_file}' is missing the required key '{required_key}'.")

    return config


def _extract_version_info(version_file: Path) -> tuple:
    """Extracts 'VERSION' and 'VERSION_DATE' (module level string constants)
    from 'version_file' via a simple, robust regex (the file is not
    imported/executed, to avoid any side effects or dependency issues)."""
    content = version_file.read_text(encoding="utf-8")

    version_match = re.search(r'^VERSION\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
    version_date_match = re.search(r'^VERSION_DATE\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)

    if version_match is None or version_date_match is None:
        raise ValueError(
            f"Could not find both 'VERSION' and 'VERSION_DATE' string constants in '{version_file}'."
        )

    return version_match.group(1), version_date_match.group(1)


def _check_history(history_file: Path, version: str) -> None:
    """Prints a warning to stderr if 'version' (the version currently found
    in version.py) has no corresponding entry in 'history_file'. Two history
    file formats are supported:
    - Markdown: a table whose first column holds version numbers, e.g.
      '| 0.12.0 | 02.02.2026 | ... |'
    - LaTeX: '\\historyversiondate{<version>}{<date>}' commands

    Raises FileNotFoundError if 'history_file' does not exist (a configured
    history_file is expected to actually exist)."""
    if not history_file.is_file():
        raise FileNotFoundError(f"history file '{history_file}' does not exist.")

    content = history_file.read_text(encoding="utf-8")
    if history_file.suffix.lower() == ".tex":
        listed_versions = re.findall(r'\\historyversiondate\{\s*([^}]+?)\s*\}', content)
    else:
        listed_versions = re.findall(r'^\|\s*([0-9][^\|]*?)\s*\|', content, re.MULTILINE)

    if version not in listed_versions:
        print(
            f"Warning: version '{version}' (from version.py) has no corresponding entry in '{history_file}'. "
            f"Please add a changelog entry for this version.",
            file=sys.stderr,
        )


def _generate_markdown(output_file: Path, version: str, version_date: str) -> None:
    """Writes the 'about_this_documentation.md' page with the component version,
    the component's release date, and the current documentation generation
    timestamp, in a clear, human readable table."""
    generated_timestamp = datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S")

    content = (
        "# About this documentation\n"
        "\n"
        "| | |\n"
        "|---|---|\n"
        f"| **Component version** | {version} |\n"
        f"| **Component release date** | {version_date} |\n"
        f"| **Documentation generated on** | {generated_timestamp} |\n"
        "\n"
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content, encoding="utf-8")
    print(f"Generated '{output_file}'")


def _run_properdocs(command: str, cwd: Path) -> int:
    """Runs the configured 'properdocs_command' (with environment variables
    expanded, e.g. '%ROBOTPYTHONPATH%') in 'cwd' and returns its exit code."""
    expanded_command = os.path.expandvars(command)
    print(f"Running documentation build in '{cwd}':\n{expanded_command}")
    result = subprocess.run(expanded_command, cwd=cwd, shell=True)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generates 'about_this_documentation.md' (component version + build timestamp) "
                    "and then triggers the 'properdocs build' documentation build."
    )
    parser.add_argument("--config", default=str(THIS_DIR / "gen_doc_config.json"),
                         help="Path to the JSON configuration file (default: 'gen_doc_config.json' "
                              "next to this script).")
    args = parser.parse_args()

    config_file = Path(args.config).resolve()
    if not config_file.is_file():
        print(f"Error: configuration file '{config_file}' does not exist.", file=sys.stderr)
        return 1

    config_dir = config_file.parent

    try:
        config = _load_config(config_file)
    except (ValueError, json.JSONDecodeError) as reason:
        print(f"Error while reading '{config_file}': {reason}", file=sys.stderr)
        return 1

    version_file = _resolve(config_dir, config["version_file"])
    output_file = _resolve(config_dir, config["output_file"])
    history_file_str = config.get("history_file")
    properdocs_cwd = _resolve(config_dir, config.get("properdocs_cwd", "."))

    if not version_file.is_file():
        print(f"Error: version file '{version_file}' does not exist.", file=sys.stderr)
        return 1

    try:
        version, version_date = _extract_version_info(version_file)
    except ValueError as reason:
        print(f"Error: {reason}", file=sys.stderr)
        return 1

    print(f"Component version: {version} ({version_date})")

    # history check is optional (see module docstring): skipped if the
    # 'history_file' key is omitted or explicitly set to 'null' in the JSON config
    if history_file_str is not None:
        history_file = _resolve(config_dir, history_file_str)
        try:
            _check_history(history_file, version)
        except FileNotFoundError as reason:
            print(f"Error: {reason}", file=sys.stderr)
            return 1

    _generate_markdown(output_file, version, version_date)

    return _run_properdocs(config["properdocs_command"], properdocs_cwd)


if __name__ == "__main__":
    sys.exit(main())
