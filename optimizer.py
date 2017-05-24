import math
import inspect


def wp(g1=0, g7=0, g8=0, c1=0):
	return math.sqrt((g1 * g8) / (g7 * c1))

def Q(g1=0, g2=0, g6=0, g7=0, g8=0, c1=0, c2=0):
	return ((g6 * c2) / (g2 * g7)) * math.sqrt((g1 * g8) / (g7 * c1))

def k(g1=0, g2=0, g4=0, g6=0, g7=0, g8=0, c1=0, c2=0):
	return ((g2 * g4) / (g6 * g c2)) * (Q(g1, g2, g6, g7, g8, c1, c2) / wp(g1, g7, g8, c1))

def BW(g1=0, g2=0, g6=0, g7=0, g8=0, c1=0, c2=0):
	return wp(g1, g7, g8, c1) / Q(g1, g2, g6, g7, g8, c1, c2)


wanted_results = {
	("wp", wp, {
		"optimal": 350,
		"allowance": (-5, 5) 
		}),
	("BW", BW, {
		"optimal": 200,
		"allowance": (-5, 5)
		}),
	("k", k, {
		"optimal": 10,
		"allowance": (-3, 3)
		})
}

parameters_limits = {
	"g1": (17E-12, 100E-12),
	"g2": (17E-12, 100E-12),
	"g4": (17E-12, 100E-12),
	"g6": (17E-12, 100E-12),
	"g7": (17E-12, 100E-12),
	"g8": (17E-12, 100E-12),
	"c1": (0.05E-15, 2E-15),
	"c2": (0.05E-15, 2E-15)
}

optimization_priority = {
	"k": .5,
	"BW": .3,
	"wp": .2
}

mutation_units = {name: (b[0]-b[1])/1000 for name, b in parameters_limits}

mutation_probability = .15


def simulate(functions, arguments):

	results = dict({})

	for name, fun in functions.items():

		needed_args = inspect.getargspec(fun)
		args_to_pass = [a for a in arguments if a in needed_args]

		results[name] = fun(args_to_pass)

	return results


def fitness(results: Dict[str, float], wanted_result, optimization_priority):

	fitnesses = dict({})

	for name, _, goals in wanted_result:

		result = results[name]

		opt = goals["optimal"]
		lower_barrier = goals["allowance"][0]
		upper_barrier = goals["allowance"][1]
		max_qdist = max([lower_barrier, upper_barrier]) ** 2

		dist = opt - result
		q_dist = dist ** 2

		if dist < lower_barrier:
			fitnesses[name] = 0
			continue

		if dist > upper_barrier:
			fitnesses[name] = 0
			continue

		fitnesses[name] = (max_qdist - q_dist) / max_qdist

	fitnesses = {optimization_priority[name] * f for name, f in fitnesses.items}
	fitness = sum(fitness.values()) / len(fitnesses)

	return fitness


def mutate(arguments: Dict[str, float]):

	mutated_args = dict({})

	for name, value in arguments.keys():
		if random.uniform(0, 1) <= mutation_probability:
			if random.choice([True, False]):
				mutated_args[name] = value + mutation_units[name]
			else:
				mutated_args[name] = value - mutation_units[name]

	return mutated_args


def generate_gen_0(size: int, parameters_limits: Dict[str, Tuple[float, float]]):
	return [{name: random.uniform(b[0], b[1]) for name, b in parameters_limits} for i in range(size)]

