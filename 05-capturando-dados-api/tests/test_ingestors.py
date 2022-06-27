import datetime
from ingestors import DataIngestor
from writers import DataWriter
from unittest.mock import patch

@patch("ingestors.DataIngestor.__abstractmethods__", set())
class TestIngestors:
    def test_checkpoint_filename(self):
        actual = DataIngestor(
            writer=DataWriter,
            coins=["TEST", "HOW"],
            default_start_date=datetime.date(2021, 6, 21)
        )._checkpoint_filename
        expected = "DataIngestor.checkpoint"
        assert actual == expected