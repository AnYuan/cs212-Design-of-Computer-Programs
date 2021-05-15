import enum
import string
import re
import itertools
import time


def valid(f):
    "Formula f is valid iff it has no numbers with leading zero, and evals true."
    try:
        # exclude digits like 0342, \b means boundary
        return not re.search(r'\b0[0-9]', f) and eval(f) is True
    except ArithmeticError:
        return False


def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    for f in fill_in(formula):
        if valid(f):
            return f


def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    letters = ''.join(set(re.findall(r'[A-Z]', formula)))  # should be a string
    for digits in itertools.permutations('1234567890', len(letters)):
        table = str.maketrans(letters, ''.join(digits))
        yield formula.translate(table)


def compile_word(word):
    """Compile a word of uppercase letters as numberic digits.
    E.g., compile_word('YOU') => '(1*U+10*0+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""
    if word.isupper():
        terms = [('%s*%s' % (10**i, d)) for (i, d) in enumerate(word[::-1])]
        return '(' + '+'.join(terms) + ')'
    else:
        return word


def timedcall(fn, *args):
    "Call function with args; return the time in seconds and return result."
    t0 = time.time()
    result = fn(*args)
    t1 = time.time()
    return t1 - t0, result


examples = """TWO + TWO == FOUR


A**2 + B**2 == C**2
A**2 + BE**2 == BY**2
X / X == X
A**N + B**N == C**N and N > 1
ATOM**0.5 == A + TO + M
GLITTERS is not GOLD
ONE < TWO and FOUR < FIVE
ONE < TWO < THREE
RAMN == R**3 + RM**3 == N**3 + RX**3
sum(range(AA)) == BB
sum(range(POP)) == BOBO
ODD + ODD == EVEN
PLUTO not in set([PLANETS])
""".splitlines()


def test():
    t0 = time.time()
    for example in examples:
        print(13*' ', example)
        print('%6.4f sec: %s ' % timedcall(solve, example))
    print('%6.4f tot.' % (time.time()-t0))


test()
