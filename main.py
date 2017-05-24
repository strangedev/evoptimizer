
def main(wanted_results :[(str, callable(dict[str, any]), dict[str, float])],
         parameter_limits :dict[str: tuple(float,float)],
         optimization_priority :dict[str:float],
         size :int,
         generation_count :int):

    gen = generate()
    i = 0
    while(i < generation_count):
        for g in gen:
            for w in wanted_results:
                simulate(w[0], w[1], w[2])

