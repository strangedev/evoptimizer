import math
import inspect
import random

# from typing import Dict, Tuple, Callable, List

def wp(g1=0, g7=0, g8=0, c1=0):
    return math.sqrt((g1 * g8) / (g7 * c1))

def Q(g1=0, g2=0, g6=0, g7=0, g8=0, c1=0, c2=0):
    return ((g6 * c2) / (g2 * g7)) * math.sqrt((g1 * g8) / (g7 * c1))

def k(g1=0, g2=0, g4=0, g6=0, g7=0, g8=0, c1=0, c2=0):
    return ((g2 * g4) / (g6 * c2)) * (Q(g1, g2, g6, g7, g8, c1, c2) / wp(g1, g7, g8, c1))
     #return g4 / g7

def BW(g1=0, g2=0, g6=0, g7=0, g8=0, c1=0, c2=0):
    return wp(g1, g7, g8, c1) / Q(g1, g2, g6, g7, g8, c1, c2)


my_wanted_results = {
    "wp": (wp, {
        "optimal": 350,
        "allowance": (-30, 30)
        }),
    "BW": (BW, {
        "optimal": 200,
        "allowance": (-30, 30)
        }),
    "k": (k, {
        "optimal": 10,
        "allowance": (-3, 3)
        })
}

my_parameters_limits = {
    "g1": (1E-12, 1E-10),
    "g2": (1E-12, 1E-10),
    "g4": (1E-12, 1E-10),
    "g6": (1E-12, 1E-10),
    "g7": (1E-12, 1E-10),
    "g8": (1E-12, 1E-10),
    "c1": (1E-15, 50E-15),
    "c2": (1E-15, 50E-15)
}

my_optimization_priority = {
    "k": .5,
    "BW": .3,
    "wp": .2
}

mutation_units = {name: (b[0]-b[1])/100000 for name, b in my_parameters_limits.items()}

mutation_probability = .15

kill_percentage = .5


def simulate(functions, arguments):

    results = dict({})

    for name, description in functions.items():
        fun = description[0]

        needed_args = inspect.getargspec(fun)[0]
        args_to_pass = {name: value for name, value in arguments.items() if name in needed_args}

        results[name] = fun(**args_to_pass)

    return results


def fitness(results, wanted_result, optimization_priority):

    fitnesses = dict({})

    for name, description in wanted_result.items():
        goals = description[1]

        result = results[name]

        opt = goals["optimal"]
        lower_barrier = goals["allowance"][0]           #will get -x
        upper_barrier = goals["allowance"][1]           #will get x
        max_qdist = max(*[lower_barrier ** 2, upper_barrier ** 2])    #always upper??

        dist = opt - result
        q_dist = dist ** 2

        if dist < lower_barrier:
            fitnesses[name] = 0
            continue

        if dist > upper_barrier:
            fitnesses[name] = 0
            continue

        fitnesses[name] = (max_qdist - q_dist) / max_qdist

    fitnesses = [optimization_priority[name] * f for name, f in fitnesses.items()]
    fitness = sum(fitnesses) / len(fitnesses)

    return fitness


def mutate(arguments, parameters_limits):

    mutated_args = dict({})

    for name, value in arguments.items():
        successfull = False

        if random.uniform(0, 1) <= mutation_probability:

            while not successfull:
                if random.choice([True, False]):
                    step = mutation_units[name]
                else:
                    step = -mutation_units[name] 

                if value + step < parameters_limits[name][0]:
                    continue
                if value + step > parameters_limits[name][1]:
                    continue

                value += step
                successfull = True

        mutated_args[name] = value

    return mutated_args


def generate_gen_0(size: int, parameters_limits):#: dict(str, tuple(float, float))):
    return [{name: random.uniform(b[0], b[1]) for name, b in parameters_limits.items()} for i in range(size)]


def __main__(wanted_results,#List[dict(str, Tuple[Callable[dict(str, any]], dict(str, float]]]],
         parameter_limits, #dict(str, tuple(float, float)),
         optimization_priority, #dict(str, float),
         size: int,
         generation_count: int):


    gen = generate_gen_0(size, parameter_limits)

    kill_count = int(kill_percentage * size)

    for i in range(generation_count):

        gen_results = []

        for args in gen:
            gen_results.append((args, simulate(wanted_results, args)))

        gen_fitnesses = []

        for args, results in gen_results:
            gen_fitnesses.append((args, results, fitness(results, wanted_results, optimization_priority)))

        gen_fitnesses = sorted(gen_fitnesses, key=lambda t: t[2])

        for kill_i in range(kill_count):
            gen_fitnesses.pop(0)

        gen_fitnesses.reverse()

        yield gen_fitnesses

        new_gen = [item[0] for item in gen_fitnesses]

        for i in range(kill_count):
            new_gen.append(mutate(gen_fitnesses[i][0], parameter_limits))

        if gen_fitnesses[0][2] == 0.0:
            new_gen = generate_gen_0(size, parameter_limits)

        gen = new_gen


for gen in __main__(my_wanted_results, my_parameters_limits, my_optimization_priority, 1000, 50000):
    print("TOP:", gen[0][2], "|\n", )#gen)