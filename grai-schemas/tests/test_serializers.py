import tempfile
from pathlib import Path

from grai_schemas.serializers import GraiYamlSerializer, dump_json, load_json


class TestGraiYamlSerializer:
    """ """

    encoder = GraiYamlSerializer()

    def test_dump(self):
        result = self.encoder.dump({"a": 1})
        assert isinstance(result, str)
        assert result == "a: 1\n"

    def test_dump_to_file(self):
        """create a file and test that it can be dumped"""
        with tempfile.NamedTemporaryFile("w+") as file:
            self.encoder.dump({"a": 1}, file)
            file.flush()
            file.seek(0)
            assert file.read() == "a: 1\n"

    def test_dump_sequence(self):
        result = self.encoder.dump([{"a": 1}, {"b": 2}])
        assert isinstance(result, str)
        assert result == "a: 1\n---\nb: 2\n"

    def test_dump_sequence_to_file(self):
        """create a file and test that it can be dumped"""
        with tempfile.NamedTemporaryFile("w+") as file:
            self.encoder.dump([{"a": 1}, {"b": 2}], file)
            file.flush()
            file.seek(0)
            assert file.read() == "a: 1\n---\nb: 2\n"

    def test_load_from_file_string(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(b"a: 1\n")
            file.flush()
            result = self.encoder.load(file.name)
            assert result == {"a": 1}

    def test_load_from_path(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(b"a: 1\n")
            file.flush()
            result = self.encoder.load(Path(file.name))
            assert result == {"a": 1}

    def test_load_from_file_io(self):
        with tempfile.NamedTemporaryFile() as file:
            file.write(b"a: 1\n")
            file.flush()
            file.seek(0)
            result = self.encoder.load(file)
            assert result == {"a": 1}

    def test_load_from_raw_string(self):
        result = self.encoder.load("a: 1\n")
        assert result == {"a": 1}

    def test_roundtrip(self):
        """test that a roundtrip from dump to load works"""
        data = [{"a": 1}, {"b": 2, "a": 3}]
        result = self.encoder.load(self.encoder.dump(data))
        assert result == data
