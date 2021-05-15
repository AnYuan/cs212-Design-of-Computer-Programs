from os import statvfs_result
import time
import itertools


def nextto(h1, h2):
    return abs(h1-h2) == 1


def imright(h1, h2):
    return h1 - h2 == 1


def zebra_puzzle():
    "Return a tuple (WATER, ZEBRA) indicating their house numbers."
    houses = first, _, middle, _, _ = [1, 2, 3, 4, 5]
    orderings = list(itertools.permutations(houses))  # 1
    return next((WATER, ZEBRA)
                for (red, green, ivory, yellow, blue) in c(orderings)
                if imright(green, ivory)  # 6
                for (Englishman, Spaniard, Ukranian, Japanese, Norwegian) in c(orderings)
                if Englishman is red  # 2
                if Norwegian is first  # 10
                if nextto(Norwegian, blue)  # 15
                for (coffee, tea, milk, oj, WATER) in c(orderings)
                if coffee is green  # 4
                if Ukranian is tea  # 5
                if milk is middle  # 9
                for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in c(orderings)
                if Kools is yellow  # 8
                if LuckyStrike is oj  # 13
                if Japanese is Parliaments  # 14
                for (dog, snails, fox, horse, ZEBRA) in c(orderings)
                if Spaniard is dog  # 3
                if OldGold is snails  # 7
                if nextto(Chesterfields, fox)  # 11
                if nextto(Kools, horse)  # 12
                )


def c(sequence):
    """
    Generate items in sequence; keeping counts as we go. 
    c.starts is the number of sequences started;
    c.items is number of items generated.
    """
    c.starts += 1
    for item in sequence:
        c.items += 1
        yield item


def instrument_fn(fn, *args):
    c.starts, c.items = 0, 0
    result = fn(*args)
    print('%s got %s with %5d iters over %7d items',
          fn.__name__, result, c.starts, c.items)


def timedcall(fn, *args):
    "Call function with args; return the time in seconds and return result."
    t0 = time.time()
    result = fn(*args)
    t1 = time.time()
    return t1 - t0, result


def timedcalls(n, fn, *args):
    "Call function n times with args; return the min, avg, and max time"
    if isinstance(n, int):
        times = [timedcall(fn, *args)[0] for _ in range(n)]
    else:
        times = []
        while sum(times) < n:
            times.append(timedcall(fn, *args)[0])
    return min(times), average(times), max(times)


def average(numbers):
    "Return the average (arithmetic mean) of a sequence of numbers."
    return sum(numbers) / float(len(numbers))


def ints(start, end=None):
    i = start
    while i <= end or end is None:
        yield i
        i = i + 1


def all_ints():
    "Generate integers in the order 0, +1, -1, +2, -2, +3, -3, ..."
    yield 0
    for i in ints(1):
        yield +i
        yield -i
