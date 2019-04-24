#!/usr/bin/python

import sys
import module

class Edge:
	def __init__(self):
		self.id #int
		self.origin #vertex
		self.destination #vertex
		self.next #edge
		self.data 
		self.quadedge #quadedge

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
		self.coordinates = coords

class QuadEdge:
	def __init__(self):
		self.edges = [0,0,0,0] #edges

#---------------------------------

filename = sys.argv[0]
f = open(filename, "r")
numvertices, dim, numattributes, numBmarkers = f.read()

vertices = lst[numvertices]
for i in range(numvertices):
	coord = f.read()
	vertices[i] = Vertex(coord)
f.close()


def MakeEdge():

def Splice(e1, e2):
def RightOf(vertex, e):
def Incircle(v1, v2, v3, v4):
def RandomEdge():

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
	elif (!RightOf(vertex, e.Onext())):
		e = e.Onext
	elif (!RightOf(vertex, e.Dprev())):
		e = e.Dprev()
	else:
		return e

def InsertSite(vertex):
		e = Locate(vertex)
		if (vertex == e.origin) or (vertex == e.destination):
			return
		elif (): #determine if point collinear
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




