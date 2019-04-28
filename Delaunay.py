#!/usr/bin/python

import sys
import numpy as np
# import ctypes
# import module

# https://www.geeksforgeeks.org/how-to-call-a-c-function-in-python/
# pred = ctype.CDLL(pred.so)
# pred.incircle.argtypes(ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,)
# pred.insphere.argtypes(ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,)
# pred.exactinit.argtypes()

# pred.exactinit()


class Edge:
	def __init__(self, id_, qe):
		self.id = id_  # int
		self.origin = "X"  # vertex
		self.destination = "X"  # vertex
		self.next = "X" #edge
		self.data = "X"
		self.quadedge = qe #quadedge


	def fix_edge(self):
		self.Sym().origin = self.destination
		self.Sym().destination = self.origin
		self.next.origin = self.origin
		self.Oprev().origin = self.origin
		self.Lprev().destination = self.origin

	def Rot(e):
		return e.quadedge.edges[(e.id + 1) % 4] #pg 95
	def Rot_inv(e):
		return e.quadedge.edges[(e.id - 1) % 4]
	def Sym(e):

		return e.Rot().Rot() #return e.quadedge.edges[(e.id + 2) % 4]
	def Onext(e):

		return e.next
	def Oprev(e):

		return e.Rot().Onext().Rot()
	def Lnext(e):
		return e.Rot_inv().Onext().Rot()
	def Lprev(e):

		return e.Onext().Sym()
	def Dprev(e):
		return e.Rot_inv().Onext().Rot_inv()

class Vertex:
	def __init__(self, coords):
		self.c = coords

class QuadEdge:
	def __init__(self):
		self.edges = [None,None,None,None] #edges

		#e Lnext=e Rnext=e Sym, and e Onext=e Oprev=e 

		self.edges[0] = Edge(0, self)
		self.edges[1] = Edge(1, self)
		self.edges[2] = Edge(2, self)
		self.edges[3] = Edge(3, self)

		self.edges[0].next = self.edges[0]
		self.edges[1].next = self.edges[3]
		self.edges[2].next = self.edges[2]
		self.edges[3].next = self.edges[1]


class Subdivision:
	def __init__(self):
		self.verticies = []
		self.edges = []
		self.faces = []

# ---------------------------------

def Splice(e1, e2): #pg 96
	a = Edge.Rot(Edge.Onext(e1))
	b = Edge.Rot(Edge.Onext(e2))

	t1 = Edge.Onext(e2)
	t2 = Edge.Onext(e1)
	t3 = Edge.Onext(b)
	t4 = Edge.Onext(a)

	e1.next = t1
	e2.next = t2
	a.next = t3
	b.next = t4
	return 

def RightOf(vertex, e):
	#https://www.cs.cmu.edu/~quake/robust.html
	if (vertex == "X"):
		bean = 1
	if (e.origin =="X"):
		beef = 1
	if (e.destination == "X"):
		been = 1
	a = np.array([[e.origin.c[0]-vertex.c[0], e.origin.c[1]-vertex.c[1]], \
		[e.destination.c[0]-vertex.c[0], e.destination.c[1]-vertex.c[1]]])
	return np.linalg.det(a.transpose())
def Incircle(v1, v2, v3, v4, v5=None):
	#https://people.eecs.berkeley.edu/~jrs/meshpapers/robnotes.pdf
	if (v1 == "X"):
		i = 1
	if (v2 == "X"):
		j = 1
	if (v3 == "X"):
		k = 1
	if (v4 == "X"):
		l = 1
	if (v5 == "X"):
		m = 1
	if (v5==None):
		a = np.array([[v1.c[0]-v4.c[0], v2.c[0]-v4.c[0], v3.c[0]-v4.c[0]], \
			[v1.c[1]-v4.c[1], v2.c[1]-v4.c[1], v3.c[1]-v4.c[1]], \
			[(v1.c[0]-v4.c[0])**2-(v1.c[1]-v4.c[1])**2, \
				(v2.c[0]-v4.c[0])**2-(v2.c[1]-v4.c[1])**2, \
				(v3.c[0]-v4.c[0])**2-(v3.c[1]-v4.c[1])**2]])
		return np.linalg.det(a.transpose())
	else:
		a = np.array([[v1.c[0]-v5.c[0], v2.c[0]-v5.c[0], v3.c[0]-v5.c[0],v4.c[0]-v5.c[0]], \
			[v1.c[1]-v5.c[1], v2.c[1]-v5.c[1], v3.c[1]-v5.c[1],v4.c[1]-v5.c[1]], \
			[v1.c[2]-v5.c[2], v2.c[2]-v5.c[2], v3.c[2]-v5.c[2],v4.c[2]-v5.c[2]], \
			[(v1.c[0]-v5.c[0])**2-(v1.c[1]-v5.c[1])**2-(v1.c[2]-v5.c[2])**2, \
				(v2.c[0]-v5.c[0])**2-(v2.c[1]-v5.c[1])**2-(v2.c[2]-v5.c[2])**2, \
				(v3.c[0]-v5.c[0])**2-(v3.c[1]-v5.c[1])**2-(v3.c[2]-v5.c[2])**2, \
				(v4.c[0]-v5.c[0])**2-(v4.c[1]-v5.c[1])**2-(v4.c[2]-v5.c[2])**2]])
		return np.linalg.det(a.transpose())

def RandomEdge():
	return qedges[0].edges[0]

def Connect(e1, e2, side=None): #pg 103
	e = MakeEdge()

	global qedges
	qedges += [e.quadedge]

	e.origin = e1.destination
	e.destination = e2.origin
	Splice(e, e1.Lnext())
	Splice(e.Sym(), e2) 
	return e

def DeleteEdge(e): #pg 103
	Splice(e, e.Oprev())
	Splice(e.Sym(), e.Sym().Oprev())
	qedges.remove(e)

def Swap(e): #pg 104
	a = e.Oprev()
	b = e.Sym().Oprev()
	Splice(e,a)
	Splice(e.Sym(), b)
	Splice(e, a.Lnext())
	Splice(e.Sym(), b.Lnext())
	e.origin = a.destination
	e.destination = b.destination

def Locate(vertex):
	e = RandomEdge()
	# DO
	while (True):
		if (vertex == e.origin or vertex == e.destination):
			return e
		elif (RightOf(vertex, e)):
			e = e.Sym()
		elif (not RightOf(vertex, e.Onext())):
			e = e.Onext()
		elif (not RightOf(vertex, e.Dprev())):
			e = e.Dprev()
		return e
	# DO

def InsertSite(vertex):

	e = Locate(vertex)

	if (vertex == e.origin) or (vertex == e.destination):
		return
	elif (RightOf(vertex, e)==0): #determine if point collinear
		t = e.Oprev()
		DeleteEdge(e)
		e = t
	base = MakeEdge()
	first = e.origin
	base.origin = first
	base.destination = vertex
	Splice(base, e)
	base.fix_edge()
	while (e.destination != first):  #infite loop
		e.fix_edge()
		base.fix_edge()
		base = Connect(e, base.Sym())
		e = base.Oprev()
	e = base.Oprev()
	e.fix_edge()
	# DO
	while (True):
		t = e.Oprev()
		if (RightOf(t.destination, e)) and Incircle(e.origin, t.destination, e.destination, vertex):
			Swap(e)
			e = t
		elif (e.origin == first):
			break;
		else:
			e = e.Onext().Lprev()
	#OF


# filename = sys.argv[1]
filename = "testfiles/4.node"
f = open(filename, "r")

vertices = f.read().split("\n")
vertices = [[float(i) for i in v.split()] for v in vertices]
numvertices, dim, numattributes, numBmarkers = vertices[0] 

dim = int(dim)
numvertices = int(numvertices)

vertices = vertices[1:numvertices+1]
for i in range(numvertices):
	vertices[i] = Vertex(vertices[i])
f.close()

qedges = []


def MakeEdge(): #pg 96
	# Takes no parameters and returns an edge e of a newly creeated data structure
	# representing a subdivision of the sphere

	# Apart from orientation and direction, e will be the
	# only edge of the subdivision and will not be a loop;

	# e Org != e Dest, e Left=e Right, e Lnext=e Rnext=e Sym, and e Onext=e Oprev=e.

	# To construct a loop, we may use et MakeEdge[ ].Rot; then we will have e Org=e Dest, eLeft
	# != e Right, e Lnext = e Rnext = e, and e Onext = e Oprev = e Sym.

	quadedge = QuadEdge()

	global qedges
	quadedge.edges[0]
	qedges += [quadedge]

	return quadedge.edges[0]


first = vertices[0]
second = vertices[1]

start = MakeEdge()
start.origin = first
start.destination = second
start.fix_edge()

vertices = vertices[2:]
for v in vertices:
	InsertSite(v)


f = open(filename[:len(filename)-4]+".ele", "a")
f.write("beans")
f.close()





