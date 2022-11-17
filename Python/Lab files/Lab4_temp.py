import numpy as np


def get_balanced_tp(supply, demand, costs, penalties=None):
    total_supply = sum(supply)
    total_demand = sum(demand)

    if total_supply < total_demand:
        new_supply = supply + [total_demand - total_supply]
        new_costs = costs + [penalties]
        return new_supply, demand, new_costs
    if total_supply > total_demand:
        new_demand = demand + [total_supply - total_demand]
        new_costs = costs + [[0 for _ in demand]]
        return supply, new_demand, new_costs
    return supply, demand, costs


def get_total_cost(costs, solution):
    total_cost = 0
    for i, row in enumerate(costs):
        for j, cost in enumerate(row):
            total_cost += cost * solution[i][j]
    return total_cost


def transportation_simplex_method(supply, demand, costs):
    balanced_supply, balanced_demand, balanced_costs = get_balanced_tp(
        supply, demand, costs
    )


if __name__ == "__main__":
    costs = [
            [21, 16, 25, 13],
            [17, 18, 14, 23],
            [32, 17, 18, 41]
    ]
    supply = [11, 13, 19]
    demand = [6, 10, 12, 15]
    solution = transportation_simplex_method(supply, demand, costs)
    print(solution)
    print('total cost: ', get_total_cost(costs, solution))
