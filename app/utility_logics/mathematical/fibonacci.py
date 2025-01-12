from typing import List

def fibonacci_sequence(n: int) -> List[int]:
    """
    Generates Fibonacci sequence up to the nth term.
    """
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i - 1] + sequence[i - 2])
    return sequence