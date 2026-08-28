#!/usr/bin/env python3
"""Validate QnA JSON data under a qna directory tree.

Checks, per version/category/value JSON file:
  - the file parses as JSON,
  - ``qnas`` is a list,
  - each item has at least one usable content field,
  - every ``qimage``/``aimage`` path exists and is an allowed image extension,
  - warn (not error) on answers with no content,
  - flag stray ``*.<non-json>`` files and binaries anywhere under ``qna/``.

Exit codes: 0 = ok (no errors or warnings), 1 = errors, 2 = warnings only.
"""

import argparse
import json
import os
from collections.abc import Callable

from app.data import IMAGE_EXTENSIONS
from app.qna_keys import LEGACY_ANSWER_KEYS, LEGACY_CONTENT_KEYS, LEGACY_IMAGE_KEYS
from app.utils import resolve_safe_image_path

NON_JSON_EXTENSIONS = {".exe", ".bin", ".so", ".dll", ".o", ".a", ".c", ".h", ".md", ".txt"}

Report = Callable[[str], object]


def validate_qna_dir(qna_dir: str, report: Report) -> tuple[int, int]:
    """Validate a qna directory tree.

    ``report`` is a callable taking a single string message line. Returns
    ``(errors, warnings)`` counts, matching the CLI exit-code semantics.
    """
    errors = 0
    warnings = 0
    qna_dir = os.path.abspath(qna_dir)

    if not os.path.isdir(qna_dir):
        report(f"ERROR: qna dir not found: {qna_dir}")
        return 1, 0

    for version in sorted(os.listdir(qna_dir)):
        ver_path = os.path.join(qna_dir, version)
        if not os.path.isdir(ver_path):
            report(f"ERROR: non-directory entry in qna root: {version}")
            errors += 1
            continue
        if version.startswith("."):
            report(f"WARN: hidden directory in qna root: {version}")
            warnings += 1
            continue
        for category in sorted(os.listdir(ver_path)):
            cat_path = os.path.join(ver_path, category)
            if not os.path.isdir(cat_path):
                if not category.startswith("."):
                    report(f"WARN: stray file in version dir: {version}/{category}")
                    warnings += 1
                continue
            if category.startswith("."):
                continue
            for dirpath, dirnames, filenames in os.walk(cat_path):
                dirnames[:] = [d for d in dirnames if not d.startswith(".")]
                base_dir = os.path.basename(dirpath)
                if base_dir == "img" or base_dir.startswith("."):
                    continue
                for filename in sorted(filenames):
                    file_path = os.path.join(dirpath, filename)
                    rel = os.path.relpath(file_path, qna_dir)
                    root, ext = os.path.splitext(filename)
                    if ext.lower() == ".json":
                        err, warn = _check_json_file(file_path, rel, qna_dir, report)
                        errors += err
                        warnings += warn
                    elif ext.lower() in NON_JSON_EXTENSIONS:
                        report(f"ERROR: stray {ext.lower().lstrip('.')} file: {rel}")
                        errors += 1
                    else:
                        report(f"WARN: non-json file: {rel}")
                        warnings += 1

    return errors, warnings


def _check_json_file(file_path: str, rel: str, qna_dir: str, report: Report) -> tuple[int, int]:
    try:
        with open(file_path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (ValueError, OSError) as exc:
        report(f"ERROR: unparseable JSON {rel}: {exc}")
        return 1, 0

    if not isinstance(data, dict):
        report(f"ERROR: {rel} top-level value is not an object")
        return 1, 0

    qnas = data.get("qnas")
    if not isinstance(qnas, list):
        report(f"ERROR: {rel}: 'qnas' is not a list")
        return 1, 0

    if not qnas:
        report(f"ERROR: {rel}: 'qnas' is empty")
        return 1, 0

    errors = 0
    warnings = 0
    for index, item in enumerate(qnas):
        if not isinstance(item, dict):
            report(f"ERROR: {rel} item {index} is not an object")
            errors += 1
            continue
        if not any(item.get(k) for k in LEGACY_CONTENT_KEYS):
            report(f"ERROR: {rel} item {index} has no usable question content (empty {{}})")
            errors += 1
        if not any(item.get(k) for k in LEGACY_ANSWER_KEYS):
            report(f"WARN: {rel} item {index} has no answer content")
            warnings += 1
        for key in LEGACY_IMAGE_KEYS:
            path = item.get(key)
            if not path:
                continue
            full = resolve_safe_image_path(qna_dir, str(path))
            if full is None:
                report(f"ERROR: {rel} item {index} {key} escapes qna root: {path}")
                errors += 1
            elif not os.path.isfile(full):
                report(f"ERROR: {rel} item {index} {key} file missing: {path}")
                errors += 1
            else:
                _, ext = os.path.splitext(full)
                if ext.lower() not in IMAGE_EXTENSIONS:
                    report(f"ERROR: {rel} item {index} {key} not an allowed image: {path}")
                    errors += 1

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate_qna",
        description="Validate QnA JSON data under a qna directory tree.",
    )
    parser.add_argument(
        "qna_dir",
        nargs="?",
        default="qna",
        help="path to the qna data directory (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    errors, warnings = validate_qna_dir(args.qna_dir, lambda line: print(line))
    print(f"\nSummary: {errors} error(s), {warnings} warning(s)")
    if errors:
        return 1
    if warnings:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
