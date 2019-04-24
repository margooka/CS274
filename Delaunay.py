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
		self.origin #vertex
		self.destination #vertex
		self.next #edge
		self.data 
		self.quadedge = QE #quadedge

	def Rot(e):
		return e.quadedge.edges[(e.id + 1) % 4]
	def Rot_inv(e):
		return e.quadedge.edges[(e.id - 1) % 4]
	def Sym(e):
		return Rot(Rot(e))
	def Onext(e):
		return e.next
	def Oprev(e):
		return Rot(Onext(Rot(e)))
	def Lnext(e):
		return Rot(Onext(Rot_inv(e)))
	def Lprev(e):
		return Sym(Onext(e))
	def Dprev(e):
		return Rot_inv(Onext(Rot_inv(e)))

class Vertex:
	def __init__(self, coords):
		self.c = coords

class QuadEdge:
	def __init__(self):
		self.edges = [None,None,None,None] #edges
		self.edges[0] = Edge.edge(0, self)
		self.edges[1] = Edge.edge(1, self)
		self.edges[2] = Edge.edge(2, self)
		self.edges[3] = Edge.edge(3, self)

		self.edges[0].next = self.edges[0]
		self.edges[1].next = self.edges[3]
		self.edges[2].next = self.edges[2]
		self.edges[3].next = self.edges[1]

#---------------------------------

filename = sys.argv[0]
f = open(filename, "r")
numvertices, dim, numattributes, numBmarkers = f.read()

vertices = lst[numvertices]
for i in range(numvertices):
	coord = f.read()
	vertices[i] = Vertex(coord)
f.close()


def MakeEdge(): #pg 96
	v1 = vertices[0]
	v2 = vertices[1]
	quadedge = QuadEdge()

MakeEdge()

f = open(filename[:len(filename)-3]+".ele", "a")
f.write()
f.close()

def Splice(e1, e2): #pg 96
	a = Rot(Onext(e1))
	b = Rot(Onext(e2))

	t1 = Onext(e2)
	t2 = Onext(e1)
	t3 = Onext(b)
	t3 = Onext(a)

	e1.next = t1
	e2.next = t2
	a.next = t3
	b.next = t4
	return 

def RightOf(vertex, e):
	#https://www.cs.cmu.edu/~quake/robust.html
	a = np.array([e.origin.c[0]-vertex.c[0], e.origin.c[1]-vertex.c[1]], \
		[e.destination.c[0]-vertex.c[0], e.destination.c[1]-vertex.c[1]])
	return np.linalg.det(a.transpose())
def Incircle(v1, v2, v3, v4, v5=None):
	#https://people.eecs.berkeley.edu/~jrs/meshpapers/robnotes.pdf
	if (v5==None):
		a = np.array([v1.c[0]-v4.c[0], v2.c[0]-v4.c[0], v3.c[0]-v4.c[0]], \
			[v1.c[1]-v4.c[1], v2.c[1]-v4.c[1], v3.c[1]-v4.c[1]], \
			[(v1.c[0]-v4.c[0])**2-(v1.c[1]-v4.c[1])**2, \
				(v2.c[0]-v4.c[0])**2-(v2.c[1]-v4.c[1])**2, \
				(v3.c[0]-v4.c[0])**2-(v3.c[1]-v4.c[1])**2])
		return np.linalg.det(a.transpose())
	else:
		a = np.array([v1.c[0]-v5.c[0], v2.c[0]-v5.c[0], v3.c[0]-v5.c[0],v4.c[0]-v5.c[0]], \
			[v1.c[1]-v5.c[1], v2.c[1]-v5.c[1], v3.c[1]-v5.c[1],v4.c[1]-v5.c[1]], \
			[v1.c[2]-v5.c[2], v2.c[2]-v5.c[2], v3.c[2]-v5.c[2],v4.c[2]-v5.c[2]], \
			[(v1.c[0]-v5.c[0])**2-(v1.c[1]-v5.c[1])**2-(v1.c[2]-v5.c[2])**2, \
				(v2.c[0]-v5.c[0])**2-(v2.c[1]-v5.c[1])**2-(v2.c[2]-v5.c[2])**2, \
				(v3.c[0]-v5.c[0])**2-(v3.c[1]-v5.c[1])**2-(v3.c[2]-v5.c[2])**2, \
				(v4.c[0]-v5.c[0])**2-(v4.c[1]-v5.c[1])**2-(v4.c[2]-v5.c[2])**2])
		return np.linalg.det(a.transpose())

def RandomEdge():
	return
def Connect(e1, e2, side=None): #pg 103
	e = MakeEdge()
	e.origin = e1.destination
	e.destination = e2.origin
	Splice(e, e1.Lnext())
	Splice(e.Sym(), e2) 

def DeleteEdge(e): #pg 103
	Splice(e, e.Oprev())
	Splice(e.Sym(), e.Sym().Oprev())

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
		e = e.Onext
	elif (not RightOf(vertex, e.Dprev())):
		e = e.Dprev()
	else:
		return e

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
	while (e.destination != first):
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




