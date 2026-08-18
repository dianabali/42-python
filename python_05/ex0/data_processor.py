"""
Data Processor

This program implements a data processing architecture based on an abstract class DataProcessor.
This class defines a common interface that all specialized data processors must follow.

DataProcessor provides two abstract methods:
    - validate() - checks whether the provided data is compatible with the processor.
    - ingest() - processes and stores valid input data.

It also provides a standard output() method that removes and returns the oldest piece of stored data together with its processing rank.

Three specialized processors inherit from DataProcessor:
    NumericProcessor:
        Accepts integers, floating-point numbers, and lists containing either type, including mixed lists.
        Numeric values are converted to strings and stored individually.
    
    TextProcessor:
        Accepts strings and lists of strings. Each string is stored separately without modification.
    
    LogProcessor:
        Accepts dictionaries containing string keys and string values, or lists of such dictionaries.
        Each log entry is converted into a formatted string containing its log level and message.

All processors store their data internally in a FIFO queue. Calling output retrieves the oldest stored item, returns its processing rank and value, and removes it from the queue.

The program also contains a main() function that demonstrates the architecture by:
    - creating an instance of each processor.
    - testing valid and invalid data with validate().
    - testing invalid ingestion without prior validation and handling the resulting exception.
    - ingesting different types of data into each processor.
    - extracting stored data using output().
"""

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._data: list[str] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Check whether data can be ingested by this processor."""
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        """Ingest data into the processor."""
        pass

    def output(self) -> tuple[int, str]:
        """Extract the oldest stored item and its processing rank."""
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
            raise ValueError("Improper numeric data")

        if isinstance(data, list):
            for item in data:
                self._data.append(str(item))
        else:
            self._data.append(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)

        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        if isinstance(data, list):
            for item in data:
                self._data.append(item)
        else:
            self._data.append(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return self._valid_log(data)

        if isinstance(data, list):
            return all(
                isinstance(item, dict) and self._valid_log(item)
                for item in data
            )

        return False

    def _valid_log(self, data: dict[Any, Any]) -> bool:
        return (
            all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in data.items()
            )
        )

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]],
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        if isinstance(data, list):
            for item in data:
                self._data.append(self._format_log(item))
        else:
            self._data.append(self._format_log(data))

    def _format_log(self, data: dict[str, str]) -> str:
        log_level = data.get("log_level", "")
        log_message = data.get("log_message", "")
        return f"{log_level}: {log_message}"


def main() -> None:
    print("=== Code Nexus - Data Processor ===")

    print()

    # Numeric Processor
    print("Testing Numeric Processor...")
    print()

    numeric = NumericProcessor()

    print("Trying to validate input '42':", numeric.validate(42))
    print("Trying to validate input 'Hello':", numeric.validate("Hello"))

    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")  # type: ignore[arg-type]
    except ValueError as error:
        print("Got exception:", error)

    print("Processing data:", [1, 2, 3, 4, 5])
    numeric.ingest([1, 2, 3, 4, 5])

    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    print("\n\n")

    # Text Processor
    print("Testing Text Processor...")
    print()

    text = TextProcessor()

    print("Trying to validate input '42':", text.validate(42))

    text_data = ["Hello", "Nexus", "World"]
    print("Processing data:", text_data)
    text.ingest(text_data)

    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    print("\n\n")

    # Log Processor
    print("Testing Log Processor...")
    print()

    log = LogProcessor()

    print("Trying to validate input 'Hello':", log.validate("Hello"))

    log_data = [
        {
            "log_level": "NOTICE",
            "log_message": "Connection to server",
        },
        {
            "log_level": "ERROR",
            "log_message": "Unauthorized access!!",
        },
    ]

    print("Processing data:", log_data)
    log.ingest(log_data)

    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
