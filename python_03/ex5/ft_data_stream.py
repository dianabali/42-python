"""
Generators allow you to iterate over data without storing the dataset in memory.
Use the 'yield' keyword.
When 'yield', the function's state is saved and the value is returned.
When the generator is called again, it continues form where it left off.
Generator parameters: Generator[yield_type, send_type, return_type]

Example:
    def my_gen():
        yield "hello"
        yield "world"
        yield 1
    for value in my_gen():
        print(value)

Another example:
    def my_gen(max):
        count = 1
        while count <= max:
            yield count
            count += 1
    result = my_gen(10)
    for value in result:
        print(value)

Anotherr examplee:
    def my_gen():
        yield "this is cool"
        yield "haha no"
        yield 42
    a = my_gen()
    print(next(a))
    print(next(a))
    print(next(a))
"""

import random
from typing import Generator

players: list[str] = ["alice", "bob", "charlie", "dylan"]
actions: list[str] = [
    "run",
    "eat",
    "sleep",
    "grab",
    "move",
    "climb",
    "swim",
    "release",
    "use"
]

def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:
        player: str = random.choice(players)
        action: str = random.choice(actions)
        yield (player, action)

def consume_event(events: list[tuple[str, str]]) -> Generator[tuple[str, str], None, None]:
    while len(events) > 0:
        index: int = random.randint(0, len(events) - 1)
        event: tuple[str, str] = events.pop(index)
        yield event

print("=== Game Data Stream Processor ===")

# Endless generator
stream: Generator[tuple[str, str], None, None] = gen_event()

# Print 1000 events
for i in range(10):
    event: tuple[str, str] = next(stream)
    print(f"Event {i}: Player {event[0]} did action {event[1]}")

# Build list of 10 events
events: list[tuple[str, str]] = []

for i in range(1000):
    events.append(next(stream))

print("Built list of 10 events:", events)

# Consume the list 
for event in consume_event(events):
    print("Got event from list:", event)
    print("Reamins in list:", events)
