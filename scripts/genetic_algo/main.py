import sys
from functools import partial
from numpy import random

from deap.tools import cxTwoPoint, mutGaussian
from scoop import shared
from termcolor import colored

from conf import indpb, sigma, partitions, selectors, strategies
from evaluation import evaluate_zen, Andividual
from evolution import evolve
import parsing

blue = partial(lambda text, color: colored(str(text), color), color='blue')
green = partial(lambda text, color: colored(str(text), color), color='green')


def main(instrument, days, popsize, strategy='trend_ema', evolvend: str=''):
    print(colored("Starting evolution....", 'blue'))
    evaluate = partial(evaluate_zen, days=days, evolvend=evolvend)
    print(blue("Evaluating ")+green(popsize)+blue(" individuals over ") + green(days) + blue(' days in ') + green(partitions) + blue(' partitions.'))
    try:
        Andividual.instruments = selectors[instrument]
    except:
        # if not in the list, assume it is one usable instrument
        Andividual.instruments = [instrument]
    Andividual.mate = cxTwoPoint
    Andividual.mutate = partial(mutGaussian, mu=0, sigma=sigma, indpb=indpb)
    # strategies = parsing.strategies()  # to use all given by list command
    # Andividual.strategies = [st for st in strategies if 'forex' not in st]
    Andividual.strategies = strategies  # to select all defined in conf.py
    Andividual.strategies = [strategy]  # to select the one given by user
    print('using strategies:', Andividual.strategies)
    print(colored(f"Mating function is ", 'blue') + colored(Andividual.mate, 'green'))
    print(colored(f"Mutating function is ", 'blue') + colored(Andividual.mutate, 'green'))
    res = evolve(evaluate, Andividual, popsize)
    return res


if __name__ == '__main__':
    INSTRUMENT = sys.argv[1]
    TOTAL_DAYS = int(sys.argv[2])
    try:
        popsize = int(sys.argv[3])
    except:
        popsize = 10
    try:
        strategy = sys.argv[4]
    except:
        strategy = 'trend_ema'
    try:
        evolvend = sys.argv[5]  # format: yyyy-mm-dd
    except:
        evolvend = ''
    print(colored("MAKE SURE YOU RUN fab backfill_local:<days>", 'red'))
    print(colored("otherwise it's all crap", 'red'))
    res = main(INSTRUMENT, TOTAL_DAYS, popsize, strategy, evolvend)
    print(res)
