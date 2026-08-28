#!/usr/bin/env python3
"""Append a QnA to a <version>/<category>/<value>.json file.

Creates the version/category directories if they are missing and appends one
QnA to the ``qnas`` list, using the same legacy keys the loader understands
(``question``/``answer``, ``qcode``/``acode``, ``cquestion``/``canswer``,
``qimage``/``aimage``).
"""

import argparse
import datetime
import json
import os


def append_qna(
    qna_dir: str,
    version: str,
    category: str,
    value: int,
    text: str | None = None,
    code: str | None = None,
    image: str | None = None,
    answer_text: str | None = None,
    answer_code: str | None = None,
    answer_image: str | None = None,
    timestamp: bool = False,
) -> str:
    """Append one QnA to the target JSON file.

    Creates missing version/category directories. Returns the absolute path to
    the JSON file that was written (or would be written).
    """
    version = str(version)
    category = str(category)
    value = int(value)
    qna_root = os.path.abspath(qna_dir)
    target_dir = os.path.join(qna_root, version, category)
    target = os.path.join(target_dir, f"{value}.json")
    os.makedirs(target_dir, exist_ok=True)

    item = {}
    if text:
        item["question"] = text
    if code:
        item["cquestion"] = code
    if image:
        item["qimage"] = image
    if answer_text:
        item["answer"] = answer_text
    if answer_code:
        item["canswer"] = answer_code
    if answer_image:
        item["aimage"] = answer_image
    if timestamp:
        item["created"] = datetime.datetime.now(datetime.UTC).isoformat()

    if os.path.isfile(target):
        with open(target, encoding="utf-8") as fh:
            data = json.load(fh)
    else:
        data = {}
    if not isinstance(data.get("qnas"), list):
        data["qnas"] = []
    data["qnas"].append(item)

    with open(target, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return os.path.abspath(target)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="create_qna",
        description="Append a QnA to a qna data file (creating dirs as needed).",
    )
    parser.add_argument("--version", required=True, help="version dir, e.g. ver1")
    parser.add_argument("--category", required=True, help="category dir, e.g. Memes")
    parser.add_argument("--value", required=True, type=int, help="integer value, e.g. 20")
    parser.add_argument("--qna-dir", default="qna", help="path to the qna data directory (default: qna)")
    parser.add_argument("--text", help="question text")
    parser.add_argument("--code", help="question code block (written as cquestion)")
    parser.add_argument("--image", help="question image path, e.g. qna/ver1/img/x.png")
    parser.add_argument("--answer", dest="answer_text", help="answer text")
    parser.add_argument("--a-code", dest="answer_code", help="answer code block (written as canswer)")
    parser.add_argument("--a-image", dest="answer_image", help="answer image path")
    parser.add_argument(
        "--timestamp",
        action="store_true",
        help="write a UTC ISO created timestamp on the new QnA",
    )
    args = parser.parse_args(argv)

    if not (args.text or args.code or args.image):
        parser.error("at least one of --text/--code/--image is required")

    target = append_qna(
        args.qna_dir,
        args.version,
        args.category,
        args.value,
        text=args.text,
        code=args.code,
        image=args.image,
        answer_text=args.answer_text,
        answer_code=args.answer_code,
        answer_image=args.answer_image,
        timestamp=args.timestamp,
    )
    print(f"Wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
