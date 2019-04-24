#!/usr/bin/python

import sys
import numpy as np
# import ctypes
#import module

#https://www.geeksforgeeks.org/how-to-call-a-c-function-in-python/
# pred = ctype.CDLL(pred.so)
# pred.incircle.argtypes(ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,)
# pred.insphere.argtypes(ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,)
# pred.exactinit.argtypes()

# pred.exactinit()

class Edge:
	def __init__(self, id_, QE):
		self.id = id_ #int
		self.origin = "X" #vertex
		self.destination = "X" #vertex
		self.next = "X" #edge
		self.data = "X"
		self.quadedge = QE #quadedge

	def Rot(e):
		return e.quadedge.edges[(e.id + 1) % 4]
	def Rot_inv(e):
		return e.quadedge.edges[(e.id - 1) % 4]
	def Sym(e):
		return Edge.Rot(Edge.Rot(e))
	def Onext(e):
		return e.next
	def Oprev(e):
		return Edge.Rot(Edge.Onext(Edge.Rot(e)))
	def Lnext(e):
		return Edge.Rot(Edge.Onext(Edge.Rot_inv(e)))
	def Lprev(e):
		return Edge.Sym(Edge.Onext(e))
	def Dprev(e):
		return Edge.Rot_inv(Edge.Onext(Edge.Rot_inv(e)))

class Vertex:
	def __init__(self, coords):
		self.c = coords

class QuadEdge:
	def __init__(self, v1, v2):
		self.edges = [None,None,None,None] #edges
		self.edges[0] = Edge(0, self)
		self.edges[1] = Edge(1, self)
		self.edges[2] = Edge(2, self)
		self.edges[3] = Edge(3, self)

		self.edges[0].next = self.edges[0]
		self.edges[1].next = self.edges[3]
		self.edges[2].next = self.edges[2]
		self.edges[3].next = self.edges[1]

		if (v1 != None):
			self.edges[0].origin = v1
			self.edges[0].destination = v2

			self.edges[1].origin = v2
			self.edges[1].destination = v1

			self.edges[2].origin = v1
			self.edges[2].destination = v2

			self.edges[1].origin = v1
			self.edges[1].destination = v2

#---------------------------------

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
	a = np.array([[e.origin.c[0]-vertex.c[0], e.origin.c[1]-vertex.c[1]], \
		[e.destination.c[0]-vertex.c[0], e.destination.c[1]-vertex.c[1]]])
	return np.linalg.det(a.transpose())
def Incircle(v1, v2, v3, v4, v5=None):
	#https://people.eecs.berkeley.edu/~jrs/meshpapers/robnotes.pdf
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
	e = MakeEdge(e1.destination, e2.origin)

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
	if (vertex == e.origin or vertex == e.destination):
		return e
	elif (RightOf(vertex, e)):
		e = e.Sym()
	elif ( not RightOf(vertex, e.Onext())):
		e = e.Onext()
	elif (not RightOf(vertex, e.Dprev())):
		e = e.Dprev()
	return e

def InsertSite(vertex):

	print("into InsertSite")

	e = Locate(vertex)

	if (vertex == e.origin) or (vertex == e.destination):
		return
	elif (RightOf(vertex, e)==0): #determine if point collinear
		t = e.Oprev()
		DeleteEdge(e)
		e = t
	base = MakeEdge(None, None)
	first = e.origin
	base.origin = first
	base.destination = vertex
	Splice(base, e)
	while (e.destination != first):  #infite loop
		print("loop")
		break;
		base = Connect(e, base.Sym())
		e = base.Oprev()
	e = base.Oprev()
	t = e.Oprev()
	if (RightOf(t.destination, e)) and Incircle(e.origin, t.destination, e.destination, vertex):
		Swap(e)
		e = t
	elif (e.origin == first):
		return
	else:
		e = e.Onext().Lprev()


filename = sys.argv[1]
f = open(filename, "r")

vertices = f.read().split("\n")
vertices = [[float(i) for i in v.split()] for v in vertices]
numvertices, dim, numattributes, numBmarkers = vertices[0] 

dim = int(dim)
numvertices = int(numvertices)

vertices = vertices[1:]
for i in range(numvertices):
	vertices[i] = Vertex(vertices[i])
f.close()

qedges = []

def MakeEdge(v1, v2): #pg 96
	quadedge = QuadEdge(v1, v2)

	global qedges
	qedges += [quadedge]

	return quadedge.edges[0]

start = MakeEdge(vertices[0], vertices[1])

for v in vertices[2:]:
	InsertSite(v)


f = open(filename[:len(filename)-4]+".ele", "a")
f.write("beans")
f.close()





