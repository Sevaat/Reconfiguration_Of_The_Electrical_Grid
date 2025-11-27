from typing import List

from src.classical_genetic_algorithm.classical_genetic_algorithm import CGA
from src.newton_method.newton_method import NewtonMethod
from src.user_function import get_fitness


def main_cga():
    cga = CGA(get_fitness)
    cga.run()

# def main_nm():
#     nm = NewtonMethod()
#     nm.run()

if __name__ == '__main__':
    main_cga()
    # main_nm()