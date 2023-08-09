from tests.mock_files.end_to_end_test.operator import Operator


class Calculate:
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
        self.operator = Operator()

    def calculate_add(self):
        return self.operator.make_addition(self.param1, self.param2)

    def calculate_multiply(self):
        print(self.param1)
        return self.operator.make_multiplication(self.param1, self.param2)


def calculator(function):
    calculate: Calculate = Calculate(param1=5, param2=10)
    if function == "add":
        return calculate.calculate_add()
    return calculate.calculate_multiply()


calculator(function="add")
