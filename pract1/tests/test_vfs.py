import hashlib
import io
import zipfile

import pytest

from vfs import VFS, VFSDir, VFSError, VFSFile


def make_zip(entries):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, data in entries.items():
            archive.writestr(name, data)
    return buffer.getvalue()


def test_minimal():
    vfs = VFS("min", make_zip({"readme.txt": "hello"}))
    node = vfs.get("/readme.txt")
    assert isinstance(node, VFSFile)
    assert node.content == "hello"
    assert not node.binary
    assert vfs.count() == (1, 0)


def test_empty_archive():
    vfs = VFS("empty", make_zip({}))
    assert vfs.root.children == {}
    assert vfs.count() == (0, 0)


def test_several_files():
    vfs = VFS("multi", make_zip({"a.txt": "a", "b.txt": "b", "c.txt": "c"}))
    assert sorted(vfs.root.children) == ["a.txt", "b.txt", "c.txt"]
    assert vfs.count() == (3, 0)


def test_deep_structure():
    data = make_zip({
        "home/user/docs/report.txt": "report",
        "etc/hosts": "127.0.0.1",
        "tmp/": "",
    })
    vfs = VFS("deep", data)
    assert isinstance(vfs.get("/home/user/docs"), VFSDir)
    assert vfs.get("home/user/docs/report.txt").content == "report"
    assert isinstance(vfs.get("/tmp"), VFSDir)
    assert vfs.count() == (2, 5)


def test_binary_file_base64():
    vfs = VFS("bin", make_zip({"image.bin": b"\x00\x01\xff"}))
    node = vfs.get("/image.bin")
    assert node.binary
    assert node.content == "AAH/"


def test_sha256():
    data = make_zip({"a.txt": "a"})
    assert VFS("a", data).sha256 == hashlib.sha256(data).hexdigest()


def test_get_missing():
    vfs = VFS("a", make_zip({"a.txt": "a"}))
    assert vfs.get("/b.txt") is None
    assert vfs.get("/a.txt/x") is None
    assert vfs.get("/") is vfs.root


def test_bad_format():
    with pytest.raises(VFSError, match="неверный формат"):
        VFS("bad", b"not a zip")


def test_file_dir_conflict():
    with pytest.raises(VFSError, match="не является папкой"):
        VFS("bad", make_zip({"a": "file", "a/b.txt": "b"}))


def test_file_not_found(tmp_path):
    with pytest.raises(VFSError, match="не удалось открыть"):
        VFS.from_file("x", tmp_path / "missing.zip")


def test_from_file_does_not_modify(tmp_path):
    path = tmp_path / "fs.zip"
    path.write_bytes(make_zip({"dir/a.txt": "a"}))
    before = path.read_bytes()
    vfs = VFS.from_file("fs", path)
    assert vfs.get("/dir/a.txt").content == "a"
    assert path.read_bytes() == before
    assert list(tmp_path.iterdir()) == [path]
