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

from app.data import IMAGE_EXTENSIONS
from app.qna_keys import LEGACY_ANSWER_KEYS, LEGACY_CONTENT_KEYS, LEGACY_IMAGE_KEYS
from app.utils import resolve_safe_image_path

NON_JSON_EXTENSIONS = {".exe", ".bin", ".so", ".dll", ".o", ".a", ".c", ".h", ".md", ".txt"}


def validate_qna_dir(qna_dir, report):
    """Validate a qna directory tree.

    ``report`` is a callable taking a single string message line. Returns
    ``(errors, warnings)`` counts, matching the CLI exit-code semantics.
    """
    errors = 0
    warnings = 0
    qna_dir = os.path.abspath(qna_dir)

    if not os.path.isdir(qna_dir):
        report("ERROR: qna dir not found: %s" % qna_dir)
        return 1, 0

    for version in sorted(os.listdir(qna_dir)):
        ver_path = os.path.join(qna_dir, version)
        if not os.path.isdir(ver_path):
            report("ERROR: non-directory entry in qna root: %s" % version)
            errors += 1
            continue
        if version.startswith("."):
            report("WARN: hidden directory in qna root: %s" % version)
            warnings += 1
            continue
        for category in sorted(os.listdir(ver_path)):
            cat_path = os.path.join(ver_path, category)
            if not os.path.isdir(cat_path):
                if not category.startswith("."):
                    report("WARN: stray file in version dir: %s/%s" % (version, category))
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
                        report("ERROR: stray %s file: %s" % (ext.lower().lstrip("."), rel))
                        errors += 1
                    else:
                        report("WARN: non-json file: %s" % rel)
                        warnings += 1

    return errors, warnings


def _check_json_file(file_path, rel, qna_dir, report):
    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (ValueError, OSError) as exc:
        report("ERROR: unparseable JSON %s: %s" % (rel, exc))
        return 1, 0

    if not isinstance(data, dict):
        report("ERROR: %s top-level value is not an object" % rel)
        return 1, 0

    qnas = data.get("qnas")
    if not isinstance(qnas, list):
        report("ERROR: %s: 'qnas' is not a list" % rel)
        return 1, 0

    if not qnas:
        report("ERROR: %s: 'qnas' is empty" % rel)
        return 1, 0

    errors = 0
    warnings = 0
    for index, item in enumerate(qnas):
        if not isinstance(item, dict):
            report("ERROR: %s item %d is not an object" % (rel, index))
            errors += 1
            continue
        if not any(item.get(k) for k in LEGACY_CONTENT_KEYS):
            report("ERROR: %s item %d has no usable question content (empty {})" % (rel, index))
            errors += 1
        if not any(item.get(k) for k in LEGACY_ANSWER_KEYS):
            report("WARN: %s item %d has no answer content" % (rel, index))
            warnings += 1
        for key in LEGACY_IMAGE_KEYS:
            path = item.get(key)
            if not path:
                continue
            full = resolve_safe_image_path(qna_dir, str(path))
            if full is None:
                report("ERROR: %s item %d %s escapes qna root: %s" % (rel, index, key, path))
                errors += 1
            elif not os.path.isfile(full):
                report("ERROR: %s item %d %s file missing: %s" % (rel, index, key, path))
                errors += 1
            else:
                _, ext = os.path.splitext(full)
                if ext.lower() not in IMAGE_EXTENSIONS:
                    report("ERROR: %s item %d %s not an allowed image: %s" % (rel, index, key, path))
                    errors += 1

    return errors, warnings


def main(argv=None):
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
    print("\nSummary: %d error(s), %d warning(s)" % (errors, warnings))
    if errors:
        return 1
    if warnings:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
