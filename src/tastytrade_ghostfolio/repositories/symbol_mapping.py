from pathlib import Path

import yaml


class SymbolMappingsNotFoundException(Exception):
    ...


class SymbolMappingRepository:
    def __init__(self):
        self.mapping_file_path = Path.cwd().joinpath("symbol_mapping.yaml")

    @staticmethod
    def _load_mapping_file(file_path: Path) -> dict[str, str]:
        with file_path.open("r") as buffer:
            return yaml.safe_load(buffer.read())

    def get_symbol_mappings(self) -> dict[str, str]:
        try:
            return self._load_mapping_file(self.mapping_file_path)

        except FileNotFoundError:
            raise SymbolMappingsNotFoundException()
