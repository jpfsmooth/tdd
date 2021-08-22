import tempfile
from pathlib import Path
import shutil
from sync import sync, determine_actions


class TestE2E:
    @staticmethod
    def test_when_a_file_exists_in_the_source_but_not_the_destination():
        try:
            source = tempfile.mkdtemp()
            dest = tempfile.mkdtemp()

            content = "I am a very useful file"
            (Path(source) / "my-file").write_text(content)

            sync(source, dest)

            expected_path = Path(dest) / "my-file"
            assert expected_path.exists()
            assert expected_path.read_text() == content

        finally:
            shutil.rmtree(source)
            shutil.rmtree(dest)

    @staticmethod
    def test_when_a_file_has_been_renamed_in_the_source():
        try:
            source = tempfile.mkdtemp()
            dest = tempfile.mkdtemp()

            content = "I am a file that was renamed"
            source_path = Path(source) / "source-filename"
            old_dest_path = Path(dest) / "dest-filename"
            expected_dest_path = Path(dest) / "source-filename"
            source_path.write_text(content)
            old_dest_path.write_text(content)

            sync(source, dest)

            assert old_dest_path.exists() is False
            assert expected_dest_path.read_text() == content

        finally:
            shutil.rmtree(source)
            shutil.rmtree(dest)


class FakeFileSystem( list):
    def copy( self, src, dest):
        self.append((' COPY', src, dest))

    def move( self, src, dest):
        self.append((' MOVE', src, dest))
  
    def delete( self, dest):
        self.append((' DELETE', src, dest))
 

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source_hashes = {"hash1": "fn1"}
    dest_hashes = {}
    actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("COPY", Path("/src/fn1"), Path("/dst/fn1"))]


def test_when_a_file_has_been_renamed_in_the_source():
    source_hashes = {"hash1": "fn1"}
    dest_hashes = {"hash1": "fn2"}
    actions = determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
    assert list(actions) == [("MOVE", Path("/dst/fn2"), Path("/dst/fn1"))]

def test_u_when_a_file_exists_in_the_source_but_not_the_destination():
    source = {" sha1": "my-file" }
    dest = {}
    filesystem = FakeFileSystem()
    reader = {"/ source": source, "/ dest": dest}
    synchronise_dirs( reader.pop, filesystem, "/ source", "/ dest")
    assert filesystem == [(" COPY", "/ source/ my-file", "/ dest/ my-file")] 

def test_u_when_a_file_has_been_renamed_in_the_source():
    source = {" sha1": "renamed-file" }
    dest = {" sha1": "original-file" }
    filesystem = FakeFileSystem()
    reader = {"/ source": source, "/ dest": dest}
    synchronise_dirs( reader.pop, filesystem, "/ source", "/ dest")
    assert filesystem == [(" MOVE", "/ dest/ original-file", "/ dest/ renamed-file")]






