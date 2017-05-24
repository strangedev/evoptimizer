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

optimization_priority = [
	"k",
	"BW",
	"wp"
]


def simulate(functions, function_names, arguments):

	results = dict({})

	for fun, name in zip(functions, function_names):

		needed_args = inspect.getargspec(fun)
		args_to_pass = [a for a in arguments if a in needed_args]

		results[name] = fun(args_to_pass)

	return results


def fitness(results, wanted_results):

	for name, _, goals in wanted_results:
		pass


