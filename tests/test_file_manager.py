import os
import shutil
import pytest

from utils.file_manager import FileManager, FileType


class TestFileManager:
    FILE_SRC_DIR = "docs_src"
    SYMBOLIC_LINK_DST = "docs_sys"

    @pytest.fixture
    def fm(self):
        yield FileManager(file_src_dir=self.FILE_SRC_DIR, symbolic_link_dst=self.SYMBOLIC_LINK_DST)
        shutil.rmtree(self.FILE_SRC_DIR)
        os.remove(self.SYMBOLIC_LINK_DST)

    def test_init(self):
        _ = FileManager(file_src_dir=self.FILE_SRC_DIR, symbolic_link_dst=self.SYMBOLIC_LINK_DST)
        assert os.path.exists(f"{self.FILE_SRC_DIR}/published")
        assert os.path.exists(f"{self.SYMBOLIC_LINK_DST}/unpublished")
        shutil.rmtree(self.FILE_SRC_DIR)
        os.remove(self.SYMBOLIC_LINK_DST)

    def test_write_unpublished(self, fm):
        fm.write("test.md", "sup", FileType.UNPUBLISHED)
        assert os.path.exists(f"{self.SYMBOLIC_LINK_DST}/unpublished/test.md")

    def test_read_unpublished(self, fm):
        file_name = "test.md"
        file_content = "sup"
        fm.write(file_name, file_content, FileType.UNPUBLISHED)
        content = fm.read(file_name, FileType.UNPUBLISHED)
        assert content == file_content

    def test_publish(self, fm):
        file_name = "test.md"
        fm.write(file_name, "sup", FileType.UNPUBLISHED)
        assert fm.publish(file_name=file_name)
