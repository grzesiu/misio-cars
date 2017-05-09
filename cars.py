import numpy as np
import math

CAR_COST = 100
MOVE_COST = 20

RENTS_1 = 3
RENTS_2 = 4
RETURNS_1 = 3
RETURNS_2 = 2

MAX_CARS = 20
MAX_MOVE = 5
DISCOUNT_FACTOR = 0.9
N_E = 5

def poisson(lam, max_n):
    f = lambda n: lam ** n * math.exp(-lam) / math.factorial(n)
    p = [f(n) for n in range(max_n + 1)]
    s = sum(p[:-1])
    probs = []
    for i in range(max_n + 1):
        probs.append([0.0] * i + p[:-i-1] + [1.0 - s])
        s -= probs[-1][-2]
    return np.array(probs, dtype=np.float)

def cars_rented(rents_no_prob):
    for (y,x) in np.ndindex(rents_no_prob.shape):
        rents_no_prob[y][x] *= rents_no_prob.shape[0] + rents_no_prob.shape[1] - y - x - 2
    return rents_no_prob

def rewards(rents1, rents2, car_cost):
    r = np.empty_like(rents1)
    for (y,x) in np.ndindex(rents1.shape):
        rents_no_prob = np.outer(rents1[y][:y + 1], rents2[x][:x + 1]) 
        r[y][x] = np.sum(car_cost * cars_rented(rents_no_prob)) 
    return r

def possible_actions(max_cars, max_move):
    shape = max_cars + 1, max_cars + 1
    possible_actions = np.empty(shape, dtype=object)
    for (y, x) in np.ndindex(shape):
        possible_actions[y][x] = np.arange(-min(x, max_cars - y, max_move), 
                min(y, max_cars - x, max_move) + 1, dtype=np.int)
        print(y, x, possible_actions[y][x])

if __name__ == "__main__":
    np.set_printoptions(formatter={'float': '{: 0.2f}'.format}, linewidth=200)

    rents1 = np.flipud(np.fliplr(poisson(RENTS_1, MAX_CARS)))
    rents2 = np.flipud(np.fliplr(poisson(RENTS_2, MAX_CARS)))
    returns1 = poisson(RETURNS_1, MAX_CARS)
    returns2 = poisson(RETURNS_2, MAX_CARS)
    
    test1 = np.array([[3,0,0],[1,2,0],[0,1,2]])
    test2 = np.array([[5,0,0],[3,2,0],[1,2,2]])
    print(rents1)
    print(rents2)
    print(rewards(rents1, rents2, CAR_COST))
    print(possible_actions(MAX_CARS, MAX_MOVE))
