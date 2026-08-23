"""
Polymorphic processing of a data stream:

This program implements an adaptive data stream processing system.
The main idea is to receive a list containing different types of data and automatically send each element to a registered processor that knows how to handle it.

The DataStream class is responsible for managing the registered processors and routing incoming data to the appropriate processor. 
A processor is selected using polymorphism: Data\stream does not need to know the concrete type of processor. Instead, it asks each processor whether it can process a particular element through the can_process() method.
"""

import typing
from abc import ABC, abstractmethod 


class DataProcessor(ABC):
    """Abstract class for all data processors"""

    @abstractmethod
    def can_process(self, data: typing.Any) -> bool:
        pass

    @abstractmethod
    def process(self, data: typing.Any) -> None:
        pass

    @abstractmethod
    def output(self, count: int) -> None:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_stats(self) -> typing.Tuple[int, int]:
        pass


class NumericProcessor(DataProcessor):
    """Processes integers and floats"""

    def __init__(self) -> None:
        self._data: list[typing.Any] = []
        self._total = 0

    def can_process(self, data: typing.Any) -> bool:
        return isinstance(data, (int, float)) and not isinstance(data, bool)

    def process(self, data: typing.Any) -> None:
        self._data.append(data)
        self._total += 1

    def output(self, count: int) -> None:
        count = min(count, len(self._data))

        for _ in range(count):
            print(self._data.pop(0))

    def get_name(self) -> str:
        return "Numeric Processor"

    def get_stats(self) -> typing.Tuple[int, int]:
        return self._total, len(self._data)


class TextProcessor(DataProcessor):
    """Processes strings"""

    def __init__(self) -> None:
        self._data: list[str] = []
        self._total = 0

    def can_process(self, data: typing.Any) -> bool:
        return isinstance(data, str)

    def process(self, data: typing.Any) -> None:
        self._data.append(data)
        self._total += 1

    def output(self, count: int) -> None:
        count = min(count, len(self._data))

        for _ in range(count):
            print(self._data.pop(0))

    def get_name(self) -> str:
        return "Text Processor"

    def get_stats(self) -> typing.Tuple[int, int]:
        return self._total, len(self._data)


class LogProcessor(DataProcessor):
    """Processes log dictionaries"""

    def __init__(self) -> None:
        self._data: list[dict[str, typing.Any]] = []
        self._total = 0

    def can_process(self, data: typing.Any) -> bool:
        return (
            isinstance(data, dict)
            and "log_level" in data
            and "log_message" in data
        )

    def process(self, data: typing.Any) -> None:
        self._data.append(data)
        self._total += 1

    def output(self, count: int) -> None:
        count = min(count, len(self._data))

        for _ in range(count):
            log = self._data.pop(0)
            print(
                "[{}] {}".format(
                    log["log_level"],
                    log["log_message"]
                )
            )

    def get_name(self) -> str:
        return "Log Processor"

    def get_stats(self) -> typing.Tuple[int, int]:
        return self._total, len(self._data)


class DataStream:
    """Routes stream elements to the appropriate data processor"""

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
    print("=== Code Nexus - Data Stream ===")
    print()
    print("Initialize Data Stream...")

    data_stream = DataStream()

    data_stream.print_processors_stats()

    print()
    print("Registering Numeric Processor")
    print()

    numeric_processor = NumericProcessor()
    data_stream.register_processor(numeric_processor)

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

    print()
    print("Registering other data processors")

    text_processor = TextProcessor()
    log_processor = LogProcessor()

    data_stream.register_processor(text_processor)
    data_stream.register_processor(log_processor)

    print("Send the same batch again")
    data_stream.process_stream(first_batch)

    data_stream.print_processors_stats()

    print()
    print("Consume some elements from the data processors:")
    print("Numeric 3, Text 2, Log 1")

    numeric_processor.output(3)
    text_processor.output(2)
    log_processor.output(1)

    data_stream.print_processors_stats()


if __name__ == "__main__":
    main()
