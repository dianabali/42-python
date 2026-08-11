from abc import ABC, abstractmethod
from typing import Any

class DataProcessor(ABC):
    def __init__(self) -> None:
        self._data: list[str] = []
        self._rank: int = 0


    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass


    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass


    def output(self) -> tuple[int, str]:
        if not self._data:
            raise IndexError("No data available")
        data = self._data.pop(0)
        rank = self._rank
        self._rank += 1
        return rank, data


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(item, (int, float)) for item in data)
        return False


    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            return ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._data.append(str(data))
        else:
            self._data.append(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return False


    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            return ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._data.append(item)
        else:
            self._data.append(data)


class LogProcessor(DataProcessor):