"""
This program is a data-routing system.
It takes a stream of mixed data and sends
each item to the first processor that knows
how to handle it.

DataProcessor is the common interface that defines
what every processor should do.

"""

from typing import Any
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    """Can I handle this data?"""
    @abstractmethod
    def can_process(self, data: Any) -> bool:
        pass

    """Check whether data can be ingested (raises on ingest if not)"""
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    """Ingest the data"""
    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    """Output some data"""
    @abstractmethod
    def output(self, count: int) -> None:
        pass

    """Return the processor's name"""
    @abstractmethod
    def get_name(self) -> str:
        pass

    """Return stats"""
    @abstractmethod
    def get_stats(self) -> tuple[int, int]:
        pass


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        self._data: list[str] = []
        self._total = 0

    def can_process(self, data: int | float | list[int | float]) -> bool:
        if isinstance(data, bool):
            return False

        if isinstance(data, (int, float)):
            return True

        if isinstance(data, list):
            return all(
                isinstance(item, (int, float)) and not isinstance(item, bool)
                for item in data
            )
        return False

    def validate(self, data: int | float | list[int | float]) -> bool:
        return self.can_process(data)

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        if isinstance(data, list):
            for item in data:
                self._data.append(str(item))
                self._total += 1
        else:
            self._data.append(str(data))
            self._total += 1

    def output(self, count: int) -> None:
        count = min(count, len(self._data))

        for _ in range(count):
            print(self._data.pop(0))

    def get_name(self) -> str:
        return "Numeric Processor"

    def get_stats(self) -> tuple[int, int]:
        return self._total, len(self._data)


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        self._data: list[str] = []
        self._total = 0

    def can_process(self, data: str | list[str]) -> bool:
        if isinstance(data, str):
            return True

        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)

        return False

    def validate(self, data: str | list[str]) -> bool:
        return self.can_process(data)

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        if isinstance(data, list):
            for item in data:
                self._data.append(item)
                self._total += 1
        else:
            self._data.append(data)
            self._total += 1

    def output(self, count: int) -> None:
        count = min(count, len(self._data))

        for _ in range(count):
            print(self._data.pop(0))

    def get_name(self) -> str:
        return "Text Processor"

    def get_stats(self) -> tuple[int, int]:
        return self._total, len(self._data)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        self._data: list[str] = []
        self._total = 0

    def can_process(
        self,
        data: dict[str, str] | list[dict[str, str]]
    ) -> bool:

        if isinstance(data, dict):
            return (
                all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in data.items()
                )
            )

        if isinstance(data, list):
            return all(
                isinstance(item, dict)
                and all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in item.items()
                )
                for item in data
            )

        return False

    def validate(
        self,
        data: dict[str, str] | list[dict[str, str]]
    ) -> bool:
        return self.can_process(data)

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        if isinstance(data, list):
            for item in data:
                self._data.append(str(item))
                self._total += 1
        else:
            self._data.append(str(data))
            self._total += 1

    def output(self, count: int) -> None:
        count = min(count, len(self._data))

        for _ in range(count):
            print(self._data.pop(0))

    def get_name(self) -> str:
        return "Log Processor"

    def get_stats(self) -> tuple[int, int]:
        return self._total, len(self._data)


class DataStream:
    """Routes stream elements to the appropriate data processor"""

    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            processed = False

            for processor in self._processors:
                if processor.can_process(element):
                    processor.ingest(element)
                    processed = True
                    break

            if not processed:
                print(
                    "DataStream error - Can't process element in stream: "
                    + str(element)
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self._processors:
            print("No processor found, no data")
            return

        for processor in self._processors:
            total, remaining = processor.get_stats()
            name = processor.get_name()

            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print()
    print("Initialize Data Stream...")

    data_stream = DataStream()

    data_stream.print_processors_stats()

    print()
    print("=== Registering Numeric Processor ===")

    numeric_processor = NumericProcessor()
    data_stream.register_processor(numeric_processor)

    my_data = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead"
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected"
            }
        ],
        42,
        ["Hi", "five"],
        True,
        [1, "some str", 2, 3.5]
    ]

    print("Send first batch of data on stream:", my_data)
    data_stream.process_stream(my_data)

    print()
    data_stream.print_processors_stats()

    print()
    print("=== Registering other data processors ===")

    text_processor = TextProcessor()
    log_processor = LogProcessor()

    data_stream.register_processor(text_processor)
    data_stream.register_processor(log_processor)

    print("Send the same batch again")
    data_stream.process_stream(my_data)

    print()
    data_stream.print_processors_stats()

    print()
    print("=== Consume some elements from the data processors ===")
    print("Numeric 3, Text 2, Log 1")

    numeric_processor.output(3)
    text_processor.output(2)
    log_processor.output(1)

    print()
    data_stream.print_processors_stats()


if __name__ == "__main__":
    main()
