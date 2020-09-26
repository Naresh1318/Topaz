import datetime
import os
import time
import pathlib
import subprocess
import functools
from enum import Enum
from typing import Tuple

import git
from git import Repo

from utils.github import extract_first_image_url


class FileType(Enum):
    PUBLISHED = 0
    UNPUBLISHED = 1


class FileManager:
    def __init__(self, file_src_dir: str, symbolic_link_dst: str):
        self.repo = Repo.init(file_src_dir)
        self.file_src_dir = pathlib.Path(file_src_dir)
        self.data_dir = pathlib.Path(symbolic_link_dst)
        self.published_dir = self.file_src_dir / "published"
        self.unpublished_dir = self.file_src_dir / "unpublished"
        if not os.path.exists(self.file_src_dir / "published"):
            os.mkdir(self.file_src_dir / "published")
        if not os.path.exists(self.file_src_dir / "unpublished"):
            os.mkdir(self.file_src_dir / "unpublished")
        if not os.path.exists(symbolic_link_dst):
            subprocess.run(["ln", "-s", file_src_dir, symbolic_link_dst])

    def read(self, file_name: str, file_type: FileType) -> str:
        data_dir = self._get_dir(file_type)
        file_path = data_dir / file_name
        if file_path.exists():
            with open(str(file_path), "r") as f:
                content = f.read()
            return content

    def write(self, file_name: str, content: str, file_type: FileType):
        assert file_type == FileType.UNPUBLISHED, "Cannot write published file"
        file_path = self.unpublished_dir / file_name
        with open(str(file_path), "w") as f:
            f.write(content)
        self._commit_file(file_name, file_type)

    def publish(self, file_name: str) -> bool:
        if file_name in self.list(as_dict=False, file_type=FileType.UNPUBLISHED):
            content = self.read(file_name, FileType.UNPUBLISHED)
            file_path = self.published_dir / file_name
            with open(str(file_path), "w") as f:
                f.write(content)
            self._commit_file(file_name, FileType.PUBLISHED)
            return True
        return False

    def unpublish(self, file_name: str) -> bool:
        if file_name in self.list(as_dict=False, file_type=FileType.PUBLISHED):
            try:
                file_path = self.published_dir / file_name
                os.remove(file_path)
                return True
            except FileNotFoundError:
                return False
        return False

    def list(self, as_dict: bool, file_type: FileType):
        data_dir = self._get_dir(file_type)
        if as_dict:
            return {str(_.name): self.get_meta(_.name, file_type) for _ in data_dir.glob("*")}
        return {str(_.name) for _ in data_dir.glob("*")}

    def delete(self, file_name: str, file_type: FileType) -> bool:
        """
        Delete both published and unpublished file

        Args:
            file_name: file to delete
            file_type: if PUBLISHED, deletes published file
                       if UNPUBLISHED, deletes, both published and unpublished file

        Returns: True  -> deleted
                 False -> not deleted

        """
        data_dir = self._get_dir(file_type)
        file_path = data_dir / file_name

        if file_name in self.list(as_dict=False, file_type=file_type):
            if file_type == FileType.PUBLISHED:
                os.remove(str(file_path))
            else:
                os.remove(str(file_path))
                assert self.delete(file_name, FileType.PUBLISHED)
            self._commit_file(file_name, file_type)
            return True
        return False

    def list_versions(self, file_name: str, file_type: FileType):
        if file_name in self.list(as_dict=False, file_type=file_type):
            commits = list(self.repo.iter_commits(paths=[str(self._get_dir(file_type) / file_name)]))
            return {c.committed_date: c.hexsha for c in commits}

    def read_version(self, file_name: str, version: str, file_type: FileType):
        if file_name in self.list(as_dict=False, file_type=file_type):
            try:
                file_path = str(self._get_dir(file_type) / file_name)
                content = self.repo.git.show(f"{version}:{file_path}")
                return content
            except git.exc.GitCommandError:
                return None

    def get_meta(self, file_name: str, file_type: FileType):
        if file_name in self.list(as_dict=False, file_type=FileType.UNPUBLISHED):
            content = self.read(file_name=file_name, file_type=file_type)
            title, description = self.extract_title_n_description(content)
            image_url = self.extract_image(content)
            git_data = self.list_versions(file_name=file_name, file_type=file_type).keys()
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(list(git_data)[0]))
            return {"file_name": file_name, "title": title, "image_url": image_url, "description": description,
                    "file_type": file_type.value, "timestamp": timestamp}

    def _commit_file(self, file_name: str, file_type: FileType):
        saved_time = self._generate_timestamp()
        data_dir = pathlib.Path("published") if file_type == FileType.PUBLISHED else pathlib.Path("unpublished")
        file_path = data_dir / file_name
        self.repo.index.add(str(file_path))
        self.repo.index.commit(f"{file_path}: {saved_time}")

    def _get_dir(self, file_type: FileType) -> pathlib.Path:
        return self.published_dir if file_type == FileType.PUBLISHED else self.unpublished_dir

    @staticmethod
    def _generate_timestamp() -> str:
        return str(datetime.datetime.now())

    @staticmethod
    @functools.lru_cache(maxsize=1024)
    def extract_title_n_description(content: str) -> Tuple[str, str]:
        title = None
        description = None
        content_lines = content.split("\n")
        i = 0
        while title is None:
            try:
                line = content_lines[i]
            except IndexError:
                return "", ""
            i += 1
            if line:
                if line.startswith("#"):
                    for i, c in enumerate(line):
                        if c != "#":
                            title = line[i:].strip()
                            break
                else:
                    title = line.strip()
            try:
                description = content_lines[i + 1]
            except IndexError:
                description = ""
        return title, description

    @staticmethod
    @functools.lru_cache(maxsize=1024)
    def extract_image(content: str) -> str:
        return extract_first_image_url(content)
