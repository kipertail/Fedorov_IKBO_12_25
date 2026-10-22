from src.main import parse


def test_parse_with_args():
    line = "ls -l /home"
    assert parse(line) == ("ls", ["-l", "/home"])


def test_parse_with_args2():
    line = "cd .."
    assert parse(line) == ("cd", [".."])


def test_parse_extra_spaces():
    line = "     ls    a   b"
    assert parse(line) == ("ls", ["a", "b"])


def test_parse_empty_line():
    line = "    "
    assert parse(line) == (None, [])
