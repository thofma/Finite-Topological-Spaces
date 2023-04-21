from Finite_Spaces.Presentations import *
from Finite_Spaces.Morse         import *

# coding: utf-8
import argparse
import sys

assert len(sys.argv) in [4, 5]

n = eval(sys.argv[1])
ni = eval(sys.argv[2])
mi = eval(sys.argv[3])
if len(sys.argv) == 5:
    number = eval(sys.argv[4])

sys.stderr.write(f'input {n} {ni} {mi}\n')

assert len(ni) == len(mi)

#n = int(sys.argv[1])
#print(n+1)

#r = 2

gens = ['x', 'y']
r1 = [('x',n), ('y',-2)]
#r2 = [('x',r), ('y',1), ('x',2), ('y',1), ('x',1-r), ('y',-1), ('x',-1), ('y',-1)]
#

ni.append(1 - sum(ni))
mi.append(1 - sum(mi))

#sys.stderr.write(f'adjusted {n} {ni} {mi}\n')

k = len(ni)
#print("adjusted input", ni, mi)

_r2 = []
for i in range(0, k):
    _r2.append(('x', ni[i]))
    _r2.append(('y', 1))
    _r2.append(('x', mi[i]))
    _r2.append(('y', -1))


sys.stderr.write(f'${_r2}\n')

rels = [r1,_r2]


def cyclic_perm(a):
    n = len(a)
    b = [[a[i - j] for i in range(n)] for j in range(n)]
    return b


def find_qstar_equivalent_presentations(gens, rels, number = 10):
    P = group_presentation(gens, rels)
    n = P.order()/4
    stdvec = [1 for x in range(n)] + [-2, -2]
    stdvec2 = [-1 for x in range(n)] + [2, 2]
    stdvec3 = [2 for x in range(n)] + [-1, -1]
    stdvec4 = [-2 for x in range(n)] + [1, 1]
    good_rels = (cyclic_perm(stdvec) + cyclic_perm(stdvec2) + cyclic_perm(stdvec3) + cyclic_perm(stdvec4))

    X = presentation_poset(gens, rels)

    l=0

    res = [];

    while l < number:
        M  = spanning_matching(X) #generate a random acyclic matching with a single critical 0-cell
        Q  = Morse_presentation(gens, rels, M)
        PP = Q.simplified()
        rel = PP.relations()
        t1 = rel[0].Tietze()
        t2 = rel[1].Tietze()

        if list(t1) in good_rels:
            assert PP.gens()[0].order() == 4 or PP.gens()[1].order() == 4
            res.append([t1, t2])
            l = l + 1

        if list(t2) in good_rels:
            assert PP.gens()[0].order() == 4 or PP.gens()[1].order() == 4
            res.append([t1, t2])
            l = l + 1

    return res

res = find_qstar_equivalent_presentations(gens, rels, number)

print(res)
