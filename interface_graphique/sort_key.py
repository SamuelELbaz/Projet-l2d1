import os


def sort_key(filename: str) -> tuple:
    base, ext = os.path.splitext(filename)
    level, num = base.split("_")[-2:]
    return level, int(num)