from __future__ import annotations
from ...platform import platform
from ...resource import Resource
from .control import ParquetControl
from ...resource import Parser


class ParquetParser(Parser):
    """JSONL parser implementation."""

    supported_types = [
        "array",
        "boolean",
        "datetime",
        "date",
        "duration",
        "integer",
        "number",
        "object",
        "string",
        "time",
    ]

    # Read

    def read_cell_stream_create(self):
        control = ParquetControl.from_dialect(self.resource.dialect)
        file = platform.fastparquet.ParquetFile(self.resource.normpath)
        for group, df in enumerate(file.iter_row_groups(**control.to_python()), start=1):
            with Resource(data=df, format="pandas") as resource:
                for line, cells in enumerate(resource.cell_stream, start=1):
                    # Starting from second group we don't need a header row
                    if group != 1 and line == 1:
                        continue
                    yield cells

    # Write

    def write_row_stream(self, source):
        platform.fastparquet.write(self.resource.normpath, source.to_pandas())