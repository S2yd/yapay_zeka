from typing import List, Tuple

import numpy as np


def route_length(order: List[int], dist_matrix: np.ndarray) -> float:
    length = 0.0
    for i in range(len(order)):
        a = order[i]
        b = order[(i + 1) % len(order)]
        length += dist_matrix[a, b]
    return length


def ant_colony_opt(
    dist_matrix: np.ndarray,
    iterations: int = 100,
    num_ants: int = 30,
    alpha: float = 1.0,
    beta: float = 3.0,
    evaporation: float = 0.5,
    q: float = 1.0,
    start_index: int = 0,
) -> Tuple[List[int], float, List[float]]:
    """
    Simple ACO for TSP. start_index is used as a fixed start node.
    """
    n = dist_matrix.shape[0]
    pheromone = np.ones((n, n))
    best_route: List[int] = []
    best_length = float("inf")
    best_history: List[float] = []

    for _ in range(iterations):
        all_routes = []
        all_lengths = []

        for _ in range(num_ants):
            start = start_index
            unvisited = [i for i in range(n) if i != start]
            route = [start]
            current = start

            while unvisited:
                probs = []
                for city in unvisited:
                    tau = pheromone[current, city] ** alpha
                    eta = (1.0 / (dist_matrix[current, city] + 1e-9)) ** beta
                    probs.append(tau * eta)

                probs = np.array(probs)
                probs = probs / probs.sum()
                next_city = np.random.choice(unvisited, p=probs)
                route.append(next_city)
                unvisited.remove(next_city)
                current = next_city

            length = route_length(route, dist_matrix)
            all_routes.append(route)
            all_lengths.append(length)

            if length < best_length:
                best_length = length
                best_route = route

        pheromone *= (1 - evaporation)
        for route, length in zip(all_routes, all_lengths):
            deposit = q / length
            for i in range(len(route)):
                a = route[i]
                b = route[(i + 1) % len(route)]
                pheromone[a, b] += deposit
                pheromone[b, a] += deposit

        best_history.append(best_length)

    return best_route, best_length, best_history
