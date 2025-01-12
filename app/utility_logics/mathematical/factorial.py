def calculate_factorial(number: int) -> int:
    """
    Calculates the factorial of a given number.
    """
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    factorial = 1
    for i in range(1, number + 1):
        factorial *= i
    return factorial
