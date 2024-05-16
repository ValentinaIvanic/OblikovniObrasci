from abc import ABC, abstractmethod
import random

class Generator(ABC):
    @abstractmethod
    def generate_numbers(self):
        pass

class SequentialGenerator(Generator):
    def __init__(self, start, end, step):
        self.start = start
        self.end = end
        self.step = step

    def generate_numbers(self):
        numbers = []
        for pom in range(self.start, self.end, self.step):
            numbers.append(pom)

        return numbers
    
class RandomGenerator(Generator):
    def __init__(self, mean, stddev, n):
        self.mean = mean
        self.stddev = stddev
        self.n = n

    def generate_numbers(self):
        numbers = []
        for i in range(self.n):
            number = int(random.normalvariate(self.mean, self.stddev))
            numbers.append(number)

        return numbers

class FibonnaciGenerator(Generator):
    def __init__(self, n):
        self.n = n

    def generate_numbers(self):
        a = 0
        b = 1
        numbers = []
        if self.n <= 0:
            return numbers
        
        numbers.append(a)
        
        if self.n > 1:
            numbers.append(b)

        for i in range(self.n - 2):
            pom = a + b
            numbers.append(pom)

            a = b
            b = pom
        
        return numbers
    

class Calculator(ABC):
    @abstractmethod
    def calculate_percentile(self, numbers, percentile):
        pass

class SortArrayCalculator(Calculator):
    def calculate_percentile(self, numbers, percentile):

        numbers = sorted(numbers)
        n_p = round(percentile*len(numbers)/100 + 0.5) + 1
        return numbers[n_p]
    
class InterpolatedCalculator(Calculator):
    def calculate_percentile(self, numbers, percentile):
        n = len(numbers)
        numbers = sorted(numbers)

        for i in range(n):
            position_vi = 100 * (i + 1 - 0.5) / n
            if (i == 0 and percentile < position_vi) or (i == n - 1 and percentile > position_vi):
                return numbers[i]
            position_vi1 = 100 * (i + 2 - 0.5) / n
            if (percentile >= position_vi and percentile <= position_vi1):
                v_p = numbers[i] + n * (percentile - position_vi) * (numbers[i + 1] - numbers[i]) / 100
                return round(v_p, 2)

class DistributionTester:

    def __init__(self, generator: Generator, calculator: Calculator):
        self.generator = generator
        self.calculator = calculator


    def test(self, count):
        numbers = self.generator.generate_numbers()
        for percentile in range(10, 100, 10):
            value = self.calculator.calculate_percentile(numbers, percentile)
            print(percentile, ". percentil: ", value)

def main():

    seq_gen = SequentialGenerator(1, 50, 2)
    sorted_calc = SortArrayCalculator()
    rand_gen = RandomGenerator(25, 0.5, 50)
    fib_gen = FibonnaciGenerator(45)
    inter_calc = InterpolatedCalculator()

    tester1 = DistributionTester(seq_gen, sorted_calc)
    tester2 = DistributionTester(rand_gen, inter_calc)
    tester3 = DistributionTester(fib_gen, sorted_calc)
    tester1.test(50)
    tester2.test(30)
    tester3.test(100)

if __name__ == "__main__":
    main()