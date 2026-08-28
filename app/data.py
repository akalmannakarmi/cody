import json
import os
import random
from typing import Any

from .qna_keys import LEGACY_CONTENT_KEYS

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
MAX_QUESTION_VALUE = 1000


class QnaStore:
    """Discovers, loads and normalizes QnA data from a qna directory tree.

    On-disk layout: ``<qna_dir>/<version>/<category>/<value>.json`` where
    ``<value>`` is an integer string (e.g. ``10``). Each JSON file wraps a
    ``qnas`` list whose items use legacy keys (``question``/``answer``,
    ``cquestion``/``canswer``, ``qcode``/``acode``, ``qimage``/``aimage``).
    """

    def __init__(self, qna_dir: str, rng: random.Random | None = None):
        self._qna_dir = os.path.abspath(qna_dir)
        self._rng = rng if rng is not None else random
        self._cache: dict[tuple[str, str, int], tuple[float, int, Any]] = {}

    @property
    def qna_dir(self) -> str:
        return self._qna_dir

    def versions(self) -> list[str]:
        if not os.path.isdir(self._qna_dir):
            return []
        return sorted(
            name
            for name in os.listdir(self._qna_dir)
            if os.path.isdir(os.path.join(self._qna_dir, name)) and not name.startswith(".")
        )

    def categories(self, version: str) -> list[str]:
        base = os.path.join(self._qna_dir, version)
        if not os.path.isdir(base):
            return []
        return sorted(
            name
            for name in os.listdir(base)
            if os.path.isdir(os.path.join(base, name)) and not name.startswith(".") and name != "img"
        )

    def values(self, version: str, category: str) -> list[int]:
        base = os.path.join(self._qna_dir, version, category)
        if not os.path.isdir(base):
            return []
        found = []
        for name in os.listdir(base):
            root, ext = os.path.splitext(name)
            if ext.lower() != ".json":
                continue
            try:
                value = int(root)
            except ValueError:
                continue
            if 0 <= value <= MAX_QUESTION_VALUE:
                found.append(value)
        return sorted(found)

    def random_question(self, version: str, category: str, value: int) -> dict[str, Any] | None:
        parsed = self._load_file(version, category, value)
        if parsed is None:
            return None
        usable = [item for item in parsed.get("qnas", []) if self._is_usable(item)]
        if not usable:
            return None
        index = self._rng.randrange(len(usable))
        return self._normalize(usable[index])

    def invalidate(self, version: str, category: str, value: int) -> None:
        self._cache.pop((version, category, value), None)

    def _file_path(self, version: str, category: str, value: int) -> str:
        return os.path.join(self._qna_dir, str(version), str(category), f"{int(value)}.json")

    def _load_file(self, version: str, category: str, value: int) -> dict[str, Any] | None:
        path = self._file_path(version, category, value)
        if not os.path.isfile(path):
            return None
        try:
            stat = os.stat(path)
            mtime = stat.st_mtime
            size = stat.st_size
        except OSError:
            return None
        key = (str(version), str(category), int(value))
        cached = self._cache.get(key)
        if cached is not None and cached[0] == mtime and cached[1] == size:
            cached_data = cached[2]
            if isinstance(cached_data, dict):
                return cached_data
            return None
        try:
            with open(path, encoding="utf-8") as fh:
                data: dict[str, Any] | None = json.load(fh)
        except (ValueError, OSError):
            data = None
        self._cache[key] = (mtime, size, data)
        return data

    @staticmethod
    def _is_usable(item: object) -> bool:
        if not isinstance(item, dict):
            return False
        return _coalesce(item, LEGACY_CONTENT_KEYS) is not None

    @staticmethod
    def _normalize(item: dict[str, Any]) -> dict[str, Any]:
        text = _coalesce(item, ("question",))
        code = _coalesce(item, ("qcode", "cquestion"))
        image = _coalesce(item, ("qimage",))
        answer_text = _coalesce(item, ("answer",))
        answer_code = _coalesce(item, ("acode", "canswer"))
        answer_image = _coalesce(item, ("aimage",))
        return {
            "text": text,
            "code": code,
            "image": _to_image_url(image),
            "answer": {
                "text": answer_text,
                "code": answer_code,
                "image": _to_image_url(answer_image),
            },
        }


def _coalesce(item: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    for key in keys:
        value = item.get(key)
        if value:
            return str(value)
    return None


def _to_image_url(path: str | None) -> str | None:
    if not path:
        return None
    return "/getImg/" + str(path).lstrip("/")
