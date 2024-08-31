from test.pytest import mod1


def summer(x: int, y: int) -> str:
    return mod1.preamable() + f"{x + y}"