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
        terms = [('%s*%s' % (10**i, d))
                 for (i, d) in enumerate(word[::-1])]  # reverse the word
        return '(' + '+'.join(terms) + ')'
    else:
        return word


def faster_solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompiles the formula; only one eval per formula."""
    f, letters = compile_formula(formula, True)
    for digits in itertools.permutations((1, 2, 3, 4, 5, 6, 7, 8, 9, 0), len(letters)):
        try:
            if f(*digits) is True:
                table = str.maketrans(letters, ''.join(map(str, digits)))
                return formula.translate(table)
        except ArithmeticError:
            pass


def compile_formula(formula, verbose=False):
    """Compile formula into a function. Also return letters found, as a str, 
    in same order as parms of function. For example, 'YOU == ME ** 2' returns
    (lambda Y, M, E, U, O: (U+10*0+100*Y) == (E+10*M)**2), 'YMEUO' """
    letters = ''.join(set(re.findall('[A-Z]', formula)))
    parms = ', '.join(letters)
    tokens = map(compile_word, re.split('([A-Z]+)', formula))
    body = ''.join(tokens)
    f = 'lambda %s: %s' % (parms, body)
    if verbose:
        print(f)
    return eval(f), letters


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
        print('%6.4f sec: %s ' % timedcall(faster_solve, example))
    print('%6.4f tot.' % (time.time()-t0))


test()
