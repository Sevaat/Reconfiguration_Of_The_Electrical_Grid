from typing import List

from src.newton_method.models.branch import Branch
from src.newton_method.newton_method import NewtonMethod

def get_fitness(genotype: List[str]) -> float:
    p_max = 1e6

    # штраф за нерадиальность
    if ((genotype[0] == "0" and genotype[2] == "0") or
        (genotype[1] == "0" and genotype[3] == "0") or
        (genotype[0] == "1" and genotype[2] == "1") or
        (genotype[1] == "1" and genotype[3] == "1")):
        return p_max

    # исключение из расчета выключенных линий
    nm = NewtonMethod()
    branches: List[Branch] = []
    for branch in nm.branches:
        if branch.start.name == "4" and branch.end.name == "5" and genotype[0] == "0":
            continue
        elif branch.start.name == "5" and branch.end.name == "6" and genotype[1] == "0":
            continue
        elif branch.start.name == "2" and branch.end.name == "5" and genotype[2] == "0":
            continue
        elif branch.start.name == "3" and branch.end.name == "6" and genotype[3] == "0":
            continue
        else:
            branches.append(branch)
    nm.branches = branches

    p = 0

    # штраф за напряжения
    nm.run()
    for node in nm.nodes:
        if node.type_node != "ИП":
            if abs(1 - abs(complex(node.real_voltage, node.imaginary_voltage)) / nm.parameters.nominal_voltage) > 0.05:
                p += p_max * abs(abs(complex(node.real_voltage, node.imaginary_voltage)) - nm.parameters.nominal_voltage)

    # штраф за токи
    for branch in nm.branches:
        if abs(branch.current) > 0.2:
            p += p_max * (abs(branch.current) / 0.2 - 1)

    # потери мощности
    p_loss = sum([branch.power_losses.real for branch in nm.branches])
    return p_loss + p