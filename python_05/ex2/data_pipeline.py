"""
Data Pipeline

This program extends the data stream processing system from Exercise 1 into
a complete data processing pipeline.

The pipeline has two main stages:
    1. Input processing: 
    DataStream receives a list containing different types of data and routes
    each element to the appropriate DataProcessor. Each processor determines
    whether it can handle an element through its can_process() method.

    2. Output processing: 
    DataStream can consume processed elements from all registered processors
    and send them to an export plugin. Export plugins can transform the
    processed data into different output formats, such as CSV or JSON.
"""

import typing
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def can_process(self, data: typing.Any) -> bool:
        pass

    @abstractmethod
    def process(self, data: typing.Any) -> None:
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
        self._data: list[typing.Any] = []
        self._total = 0
        self._next_id = 0

    def can_process(self, data: typing.Any) -> bool:
        return isinstance(data, (int, float)) and not isinstance(data, bool)

    def process(self, data: typing.Any) -> None:
        self._data.append(data)
        self._total += 1

    def output(self, count: int) -> list[tuple[int, str]]:
        result = []

        count = min(count, len(self._data))

        for _ in range(count):
            data = self._data.pop(0)
            result.append((self._next_id, str(data)))
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
        self._next_id = 0

    def can_process(self, data: typing.Any) -> bool:
        return isinstance(data, str)

    def process(self, data: typing.Any) -> None:
        self._data.append(data)
        self._total += 1

    def output(self, count: int) -> list[tuple[int, str]]:
        result = []

        count = min(count, len(self._data))

        for _ in range(count):
            data = self._data.pop(0)
            result.append((self._next_id, str(data)))
            self._next_id += 1

        return result

    def get_name(self) -> str:
        return "Text Processor"

    def get_stats(self) -> tuple[int, int]:
        return self._total, len(self._data)


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        self._data: list[dict[str, typing.Any]] = []
        self._total = 0
        self._next_id = 0

    def can_process(self, data: typing.Any) -> bool:
        return (
            isinstance(data, dict)
            and "log_level" in data
            and "log_message" in data
        )

    def process(self, data: typing.Any) -> None:
        self._data.append(data)
        self._total += 1

    def output(self, count: int) -> list[tuple[int, str]]:
        result = []

        count = min(count, len(self._data))

        for _ in range(count):
            data = self._data.pop(0)

            value = "{}: {}".format(
                data["log_level"],
                data["log_message"]
            )

            result.append((self._next_id, value))
            self._next_id += 1

        return result

    def get_name(self) -> str:
        return "Log Processor"

    def get_stats(self) -> tuple[int, int]:
        return self._total, len(self._data)


class ExportPlugin(typing.Protocol):
    def process_output(
        self,
        data: list[tuple[int, str]]
    ) -> None:
        ...


class CSVExportPlugin:
    """Export plugin that outputs data as CSV"""

    def process_output(
        self,
        data: list[tuple[int, str]]
    ) -> None:
        values = []

        for _, value in data:
            values.append(value)

        print("CSV Output: " + ",".join(values))


class JSONExportPlugin:
    """Export plugin that outputs data as JSON"""

    def process_output(
        self,
        data: list[tuple[int, str]]
    ) -> None:
        items = []

        for item_id, value in data:
            items.append(
                '"item_{}": "{}"'.format(
                    item_id,
                    value.replace('"', '\\"')
                )
            )

        print("JSON Output: {" + ", ".join(items) + "}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        for element in stream:
            processed = False

            for processor in self._processors:
                if processor.can_process(element):
                    processor.process(element)
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
            plugin.process_output(data)

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self._processors:
            print("No processor found, no data")
            return

        for processor in self._processors:
            total, remaining = processor.get_stats()

            print(
                "{}: total {} items processed, remaining {} on processor".format(
                    processor.get_name(),
                    total,
                    remaining
                )
            )


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print()
    print("Initialize Data Stream...")
    print()

    data_stream = DataStream()
    data_stream.print_processors_stats()

    print("Registering Processors")

    numeric_processor = NumericProcessor()
    text_processor = TextProcessor()
    log_processor = LogProcessor()

    data_stream.register_processor(numeric_processor)
    data_stream.register_processor(text_processor)
    data_stream.register_processor(log_processor)

    first_batch = [
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

    print("Send first batch of data on stream:", first_batch)
    data_stream.process_stream(first_batch)

    data_stream.print_processors_stats()

    print(
        "Send 3 processed data from each processor to a CSV plugin:"
    )

    csv_plugin = CSVExportPlugin()
    data_stream.output_pipeline(3, csv_plugin)

    data_stream.print_processors_stats()

    second_batch = [
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

    print("Send another batch of data:", second_batch)
    data_stream.process_stream(second_batch)

    data_stream.print_processors_stats()

    print(
        "Send 5 processed data from each processor to a JSON plugin:"
    )

    json_plugin = JSONExportPlugin()
    data_stream.output_pipeline(5, json_plugin)

    data_stream.print_processors_stats()


if __name__ == "__main__":
    main()
