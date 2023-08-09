from tests.mock_files.end_to_end_test.refactored_operator import CalculatorHelper


class Calculator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.calculator_helper = CalculatorHelper()

    def add_operation(self):
        return self.calculator_helper.add(self.x, self.y)

    def multiply_operation(self):
        print(self.x)
        return self.calculator_helper.multiply(self.x, self.y)


def make_calculations(operation):
    calculate: Calculator = Calculator(x=5, y=10)
    if operation == "add":
        return calculate.add_operation()
    return calculate.multiply_operation()


make_calculations(operation="add")
