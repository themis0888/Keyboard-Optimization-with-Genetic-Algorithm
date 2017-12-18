from solution import Solution
from config import CONFIG
from GA_algorithm import run_GA

# main function
if __name__ == '__main__':
	result = run_GA()
	result[0].plot()

