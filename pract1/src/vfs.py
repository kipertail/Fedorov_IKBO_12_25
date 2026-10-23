import base64
import hashlib
import io
import zipfile


class VFSError(Exception):
    pass


class VFSFile:
    def __init__(self, name, data):
        self.name = name
        try:
            self.content = data.decode("utf-8")
            self.binary = False
        except UnicodeDecodeError:
            self.content = base64.b64encode(data).decode("ascii")
            self.binary = True


class VFSDir:
    def __init__(self, name):
        self.name = name
        self.children = {}


class VFS:
    def __init__(self, name, data):
        self.name = name
        self.sha256 = hashlib.sha256(data).hexdigest()
        self.root = VFSDir("/")
        self._load(data)

    @classmethod
    def from_file(cls, name, path):
        try:
            with open(path, "rb") as file:
                data = file.read()
        except OSError as err:
            raise VFSError(f"не удалось открыть {path}: {err.strerror}")
        return cls(name, data)

    def _load(self, data):
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for info in archive.infolist():
                    self._add(archive, info)
        except (zipfile.BadZipFile, zipfile.LargeZipFile) as err:
            raise VFSError(f"неверный формат: {err}")

    def _add(self, archive, info):
        parts = [part for part in info.filename.split("/") if part]
        if not parts:
            return
        if info.is_dir():
            self._make_dirs(parts)
            return
        parent = self._make_dirs(parts[:-1])
        name = parts[-1]
        if name in parent.children:
            raise VFSError(f"неверный формат: дубликат {info.filename}")
        parent.children[name] = VFSFile(name, archive.read(info))

    def _make_dirs(self, parts):
        node = self.root
        for part in parts:
            child = node.children.setdefault(part, VFSDir(part))
            if not isinstance(child, VFSDir):
                raise VFSError(f"неверный формат: {part} не является папкой")
            node = child
        return node

    def count(self):
        files, dirs = 0, 0
        stack = [self.root]
        while stack:
            node = stack.pop()
            for child in node.children.values():
                if isinstance(child, VFSDir):
                    dirs += 1
                    stack.append(child)
                else:
                    files += 1
        return files, dirs

    def get(self, path):
        node = self.root
        for part in path.split("/"):
            if not part:
                continue
            if not isinstance(node, VFSDir) or part not in node.children:
                return None
            node = node.children[part]
        return node
