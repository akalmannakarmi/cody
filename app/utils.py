"""Shared utility functions for path safety and validation."""

import os


def resolve_safe_image_path(qna_dir, rel_path):
    """Resolve a relative image path safely within the qna directory.

    Returns the absolute path if safe, or None if the path escapes the root.
    """
    root = os.path.realpath(qna_dir)
    base = os.path.dirname(root)
    full = os.path.realpath(os.path.join(base, rel_path))
    if not full.startswith(root + os.sep):
        return None
    return full