

# This file was *autogenerated* from the file Finite_Spaces/Morse.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_2 = Integer(2); _sage_const_3 = Integer(3)
from Finite_Spaces.General       import *
from Finite_Spaces.Homotopy      import *
from Finite_Spaces.Presentations import *

#Morse presentation

def attaching(gens, rels):
	'''
	Computes the original attaching map of each 2-cell in the barycentric subdivision of the standard complex associated to the presentation <gens|rels>.
	INPUT: list of generators and relators in tuple format, e.g x**2 is written as [('x', 2)]
	OUTPUT: dictionary of 2-cells: an ordered list of oriented 1-cells in format (cell, +1 or - 1). 
 	'''
	att = {} #dictionary of attaching maps
	
	#expanded relations of the presentation
	Rels=[]
	for i in range(len(rels)):
		Rels.append([])
		for l in rels[i]:
			if l[_sage_const_1 ] < _sage_const_0 :
				Rels[i] += [(l[_sage_const_0 ],-_sage_const_1 ) for k in range(abs(l[_sage_const_1 ]))]
			if l[_sage_const_1 ] > _sage_const_0 :
				Rels[i] += [(l[_sage_const_0 ],_sage_const_1 ) for k in range(abs(l[_sage_const_1 ]))]
 
	for i in range(len(Rels)):
		letters = {}
		R = Rels[i]
		for (l,e) in R:
			letters[l] = _sage_const_0 
		for j in range(len(R)):
			(l,e) = R[j]
			letters[l] += _sage_const_1 
			if(e == _sage_const_1 ):
				att[aux_label(i+_sage_const_1 ,l,'2',letters[l])] = [(l+'2',_sage_const_1 ),(aux_label(i+_sage_const_1 ,l,'1',letters[l]),-_sage_const_1 ),(aux_label(i+_sage_const_1 ,_sage_const_0 ,'',j+_sage_const_1 ),_sage_const_1 )]
				att[aux_label(i+_sage_const_1 ,l,'3',letters[l])] = [(l+'3',_sage_const_1 ),(aux_label(i+_sage_const_1 ,_sage_const_0 ,'',(j+_sage_const_1 )%(len(R))+_sage_const_1 ),-_sage_const_1 ), (aux_label(i+_sage_const_1 ,l,'1',letters[l]),_sage_const_1 )]
			else:
				att[aux_label(i+_sage_const_1 ,l,'2',letters[l])] = [(l+'2',-_sage_const_1 ),(aux_label(i+_sage_const_1 ,_sage_const_0 ,'',(j+_sage_const_1 )%(len(R))+_sage_const_1 ),-_sage_const_1 ),(aux_label(i+_sage_const_1 ,l,'1',letters[l]),_sage_const_1 )]
				att[aux_label(i+_sage_const_1 ,l,'3',letters[l])] = [(l+'3',-_sage_const_1 ),(aux_label(i+_sage_const_1 ,l,'1',letters[l]),-_sage_const_1 ),(aux_label(i+_sage_const_1 ,_sage_const_0 ,'',j+_sage_const_1 ),_sage_const_1 )]
	
	return att

# auxiliary function for attaching_Morse
def write(edge, isolate):
	global new_attaching
	new_attaching = []
	return (aux_write(edge, isolate))

# auxiliary function for attaching_Morse
def aux_write(edge, isolate):
	global new_attaching
	if edge in isolate.keys():
		if isolate[edge] == []:
			return new_attaching
		for edge in isolate[edge]:
			aux_write(edge, isolate)
		return new_attaching
	else:
		new_attaching += [edge]
		return new_attaching

def attaching_Morse(attaching, M, critical_dim_2):
	'''
	Computes the attaching map of each 2-cell in the Morse complex associated to the acyclic matching M.
	INPUT: 
	- attaching: the dictionary of original attaching maps of 2-cells
	- M: acyclic matching 
	- critical_dim_2: the list of critical cells of dimension 2
 	'''
	dim2 = [] # cells of dimension 2 that collapse
	isolate = {}
	for (c1,c2) in M:
		if c2 in attaching.keys(): # c2 of dimension 2
			dim2.append(c2)
			att = [] # new attaching map of c1
			orient = _sage_const_1 
			
			for (cell,e) in attaching[c2]:
				if cell != c1:
					att.append((cell,-e))
				else:
					orient = e
					break
			att = att[::-_sage_const_1 ] # reverse list
			
			for (cell,e) in reversed(attaching[c2]):
				if cell != c1:
					att.append((cell,-e))
				else:
					break

			if orient == -_sage_const_1 :
				att = att[::-_sage_const_1 ] # reverse list
				for i in range(len(att)): # inverse of every cell
					(cell,e) = att[i]
					att[i] = (cell,-e)
			isolate[(c1,_sage_const_1 )] = att
			att_inv = []
			for i in range(len(att)): # inverse of every cell
				(cell,e) = att[i]
				att_inv.append((cell,-e))
				
			att_inv = att_inv[::-_sage_const_1 ]
			
			isolate[(c1,-_sage_const_1 )] = att_inv
		else:
			isolate[(c2,_sage_const_1 )] = []
			isolate[(c2,-_sage_const_1 )] = []
  
	d = {}
	for c in critical_dim_2:
		rel = []
		for edge in attaching[c]:
			rel += write(edge, isolate)
		d[c] =  rel
	
	return d


def att_to_group(att, gens):
	F = FreeGroup(len(gens), 'a')
	d = {}
	for i in range(len(gens)):
	   d[gens[i]] = F.gens()[i]
	Rels = []
	for c in att.keys():
		aux = F.one()
		for (cell,e) in att[c]:
			aux *= d[cell]**e
		Rels.append(aux)
	return F / Rels


def critical_by_level(X, M): 
	'''
	Return the list of critical points in X associated to the matching M for each level in the face poset
	INPUT:
	- X: poset (face poset of a regular CW)
	- M: (an acyclic) matching 
	'''
	matched = [e[_sage_const_0 ] for e in M] + [e[_sage_const_1 ] for e in M]
	edges = X.cover_relations()
	G = DiGraph(edges)
	l = G.level_sets()
	C = []
	for i in range(len(l)):
		cr = []
		for x in l[i]:
			if x not in matched:
				cr.append(x)
		C.append(cr)
	return C

def Morse_presentation(gens, rels, M):
	'''
	Returns the Morse presentation associated to the original presentation <gens|rels> and the matching M.
	'''
	original_attaching = attaching(gens,rels)
	X = presentation_poset(gens,rels)
	critical_cells = critical_by_level(X, M)
	Morse_pres = att_to_group(attaching_Morse(original_attaching, M, critical_cells[_sage_const_2 ]), critical_cells[_sage_const_1 ])
	return Morse_pres



#Matchings

def induced_spanning_tree(X,M):
    '''
    Return the induced spanning tree
    INPUT:
    - X face poset of a regular CW-complex
    - M matching in X with unique critical 0-cell
    '''
    T = []
    for e in M:
        P = X.subposet(X.order_ideal([e[_sage_const_1 ]]))
        if P.height()<_sage_const_3 :
            T.append(e)
    return T
	

import random
def greedy_acyclic_matching(X):
	'''
	Greedy algorithm that ouputs a random maximal matching.
	INPUT: X the face poset of regular CW.
	'''
	edges = X.cover_relations()
	in_match = {}
	for v in X.list():
		in_match[v] = False
	seed()
	shuffle(edges)
	M = []
	for e in edges:
		if(in_match[e[_sage_const_0 ]] or in_match[e[_sage_const_1 ]]):
			continue
		D = DiGraph(edges)
		D.reverse_edge(e)

		if D.is_directed_acyclic():
			edges.remove(e)
			edges.append([e[_sage_const_1 ], e[_sage_const_0 ]])
			M.append(e)
			in_match[e[_sage_const_0 ]] = True
			in_match[e[_sage_const_1 ]] = True
	return M

def spanning_matching(X):
	M = []
	n = _sage_const_0 
	while n != _sage_const_1 :
		M = greedy_acyclic_matching(X)
		n = len(critical_by_level(X, M)[_sage_const_0 ]) == _sage_const_1 
	return M
    
def is_acyclic(X, M):
    edges = X.cover_relations()
    D = DiGraph(edges)
    for e in M:
        D.reverse_edge(e)
    return D.is_directed_acyclic()


#Incidence of critical cells

def critical_points(X, M): #X the face poset of a regular CW, M an acyclic matching
	L = X.list()
	for e in M:
		L.remove(e[_sage_const_0 ])
		L.remove(e[_sage_const_1 ])
	return L

#Ouputs the reversed Hasse diagram of X according to M
def reverse(X, M): #X the face poset of a regular CW, M an acyclic matching
	edges = X.cover_relations()
	for e in M:
		edges.remove(list(e))
		edges.append([e[_sage_const_1 ], e[_sage_const_0 ]])
	return DiGraph(edges)

#Ouputs the incidence of y in x in K_M
def critical_incidence(gens, rels, M, x, y): #X the face poset of a regular CW (say K), M an acyclic matching, y of height i+1, x of height i. 
	X = presentation_poset(gens,rels)
	incidence = attaching(gens,rels)
	D = reverse(X,M)
	L = D.all_simple_paths(starting_vertices = [x], ending_vertices = [y])
	inc = _sage_const_0 
	for p in L: 
		s = incidence(p[_sage_const_0 ], p[_sage_const_1 ])
		for i in range(_sage_const_2 , len(p), _sage_const_2 ):
			s = s * incidence(p[i], p[i-_sage_const_1 ]) * incidence(p[i], p[i+_sage_const_1 ])
			inc = inc + s * (-_sage_const_1 )**(len(p)/_sage_const_2  - _sage_const_1 )
	return inc

def critical_CW_incidence(gens, rels, M): #X the face poset of a regular CW, M an acyclic matching
	X = presentation_poset(gens, rels)
	C = critical_by_level(X, M)
	inc = {}
	for i in range(len(C)-_sage_const_1 ):
		if C[i] != [] and C[i+_sage_const_1 ] != []:
			for y in C[i+_sage_const_1 ]:
				for x in C[i]:
					inc[(x, y)] = critical_incidence(gens, rels, M, x, y)
	return inc

