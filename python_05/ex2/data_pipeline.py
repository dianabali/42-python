"""
This program is a data-processing pipeline framework.
    1. Take data.
    2. Send each data to the right processor.
    3. Process it.
    4. Export the processed data in a CSV/JSON format.
"""


from typing import Any, Protocol
from abc import ABC, abstractmethod


class ExportPlugin(Protocol):
    """
        Any object that want to be used as an export plugin
        must have a process_output()
    """
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...
    """
        Duck typing:
            If an object behaves like the thing you need,
            you can use it like that thing.
    """
    """
        Protocol:
            Any object that has these methods can be treated as this type
    """


class DataProcessor(ABC):
    @abstractmethod
    def can_process(self, data: Any) -> bool:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    @abstractmethod
    def output(self, count: int) -> list[tuple[int, str]]:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_stats(self) -> tuple[int, int]:
        pass


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        self._data: list[str] = []
        self._total = 0
        self._next_id = 1

    def can_process(
        self,
        data: int | float | list[int | float]
    ) -> bool:
        if isinstance(data, bool):
            return False

        if isinstance(data, (int, float)):
            return True

        if isinstance(data, list):
            return all(
                isinstance(item, (int, float))
                and not isinstance(item, bool)
                for item in data
            )

        return False

    def validate(
        self,
        data: int | float | list[int | float]
    ) -> bool:
        return self.can_process(data)

    def ingest(
        self,
        data: int | float | list[int | float]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        if isinstance(data, list):
            for item in data:
                self._data.append(str(item))
                self._total += 1
        else:
            self._data.append(str(data))
            self._total += 1

    def output(self, count: int) -> list[tuple[int, str]]:
        count = min(count, len(self._data))
        result: list[tuple[int, str]] = []

        for _ in range(count):
            result.append((self._next_id, self._data.pop(0)))
            self._next_id += 1

        return result

    def get_name(self) -> str:
        return "Numeric Processor"

    def get_stats(self) -> tuple[int, int]:
        return self._total, len(self._data)


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        self._data: list[str] = []
        self._total = 0
        self._next_id = 1

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

    def output(self, count: int) -> list[tuple[int, str]]:
        count = min(count, len(self._data))
        result: list[tuple[int, str]] = []

        for _ in range(count):
            result.append((self._next_id, self._data.pop(0)))
            self._next_id += 1

        return result

    def get_name(self) -> str:
        return "Text Processor"

    def get_stats(self) -> tuple[int, int]:
        return self._total, len(self._data)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        self._data: list[str] = []
        self._total = 0
        self._next_id = 1

    def can_process(
        self,
        data: dict[str, str] | list[dict[str, str]]
    ) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in data.items()
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
                self._data.append(
                    f"{item.get('log_level')}: "
                    f"{item.get('log_message')}"
                )
                self._total += 1
        else:
            self._data.append(
                f"{data.get('log_level')}: "
                f"{data.get('log_message')}"
            )
            self._total += 1

    def output(self, count: int) -> list[tuple[int, str]]:
        count = min(count, len(self._data))
        result: list[tuple[int, str]] = []

        for _ in range(count):
            result.append((self._next_id, self._data.pop(0)))
            self._next_id += 1

        return result

    def get_name(self) -> str:
        return "Log Processor"

    def get_stats(self) -> tuple[int, int]:
        return self._total, len(self._data)


class CSVExportPlugin:
    """
        CSV - comma-separated values
        (simple text format for tabular data)
    """
    def process_output(self, data: list[tuple[int, str]]) -> None:
        values = [value for _, value in data]
        print("CSV Output:")
        print(",".join(values))


class JSONExportPlugin:
    """
        JSON - JavaScript Object Notation
        (structured text format used to exchange data between programs)
    """
    def process_output(self, data: list[tuple[int, str]]) -> None:
        result: list[str] = []

        for item_id, value in data:
            escaped_value = value.replace("\\", "\\\\")
            escaped_value = escaped_value.replace('"', '\\"')
            escaped_value = escaped_value.replace("\n", "\\n")

            result.append(
                f'"item_{item_id}": "{escaped_value}"'
            )

        print("JSON Output:")
        print("{" + ", ".join(result) + "}")


class DataStream:
    """Routes stream elements to the appropriate data processor."""

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

    def output_pipeline(
        self,
        nb: int,
        plugin: ExportPlugin
    ) -> None:
        for processor in self._processors:
            data = processor.output(nb)

            if data:
                plugin.process_output(data)

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
    print("=== Code Nexus - Data Pipeline ===")
    print()
    print("Initialize Data Stream...")
    print()

    data_stream = DataStream()

    data_stream.print_processors_stats()

    print()
    print("=== Registering Processors ===")

    numeric_processor = NumericProcessor()
    text_processor = TextProcessor()
    log_processor = LogProcessor()

    data_stream.register_processor(numeric_processor)
    data_stream.register_processor(text_processor)
    data_stream.register_processor(log_processor)

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
        ["Hi", "five"]
    ]

    print("Send first batch of data on stream:", my_data)
    data_stream.process_stream(my_data)

    print()
    data_stream.print_processors_stats()

    print()
    print("=== Send 3 processed data from each processor to a CSV plugin ===")

    csv_plugin = CSVExportPlugin()
    data_stream.output_pipeline(3, csv_plugin)

    print()
    data_stream.print_processors_stats()

    my_data2 = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash"
            },
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days"
            }
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello"
    ]

    print()
    print("Send another batch of data:", my_data2)
    data_stream.process_stream(my_data2)

    print()
    data_stream.print_processors_stats()

    print()
    print("=== Send 5 processed data from each processor to a JSON plugin ===")

    json_plugin = JSONExportPlugin()
    data_stream.output_pipeline(5, json_plugin)

    print()
    data_stream.print_processors_stats()


if __name__ == "__main__":
    main()
    
