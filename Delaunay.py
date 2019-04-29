#!/usr/bin/python

import sys
import numpy as np
import random
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
		self.id = id_
		self.origin = "X"
		self.destination = "X"
		self.next = "X"
		self.data = "X"
		self.quadedge = qe
		self.seen = False
		self.name = None


	def fix_edge(self):
		self.Sym().origin = self.destination
		self.Sym().destination = self.origin
		self.next.origin = self.origin
		self.Oprev().origin = self.origin
		self.Lprev().destination = self.origin
		self.Dnext().destination = self.destination

	def Rot(e):
		return e.quadedge.edges[(e.id + 1) % 4] #pg 95
	def Rot_inv(e):
		return e.quadedge.edges[(e.id + 3) % 4]
	def Sym(e):
		return e.Rot().Rot()
		#return e.quadedge.edges[(e.id + 2) % 4]
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
	def Dnext(e):
		return e.Sym().Onext().Sym()

class Vertex:
	def __init__(self, coords, node):
		self.c = coords
		self.Node = node

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

# ---------------------------------

def Splice(e1, e2): #pg 96
	a = e1.Onext().Rot()
	b = e2.Onext().Rot()

	c1 = e2.Onext()
	c2 = e1.Onext()
	c3 = b.Onext()
	c4 = a.Onext()

	e1.next = c1
	e2.next = c2
	a.next = c3
	b.next = c4

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
	# return random.choice(qedges).edges[0] <--- I should use this one

def Connect(e1, e2, side=None): #pg 103
	ed = MakeEdge()

	global qedges
	if ed.quadedge not in qedges:
		qedges += [ed.quadedge]

	ed.origin = e1.destination
	ed.destination = e2.origin
	ed.fix_edge()
	Splice(ed, e1.Lnext())
	Splice(ed.Sym(), e2)
	return ed

def DeleteEdge(e): #pg 103
	Splice(e, e.Oprev())
	Splice(e.Sym(), e.Sym().Oprev())
	qedges.remove(e.quadedge)

def Swap(e): #pg 104
	a = e.Oprev()
	b = e.Sym().Oprev()
	Splice(e,a)
	Splice(e.Sym(), b)
	Splice(e, a.Lnext())
	Splice(e.Sym(), b.Lnext())
	e.origin = a.destination
	e.destination = b.destination
	e.fix_edge()

def Locate(vertex):
	ed = RandomEdge()
	# lst = []
	while True:
		# print("loop")
		if vertex == ed.origin or vertex == ed.destination:
			return ed
		elif RightOf(vertex, ed) > 0.0:
			ed = ed.Sym()
			# lst += [ed] DEBUGGING
		elif RightOf(vertex, ed.Onext()) <= 0.0:
			# lst += [ed] DEBUGGING
			ed = ed.Onext()
		elif RightOf(vertex, ed.Dprev()) <= 0.0:
			# lst += [ed] DEBUGGING
			ed = ed.Dprev()
		return ed #this line is incorrect; it should be in an else block however it enters an infinite loop

def InsertSite(vertex):
	e = Locate(vertex)

	if (vertex == e.origin) or (vertex == e.destination):
		return
	elif RightOf(vertex, e) == 0.0: #determine if point collinear
		t = e.Oprev()
		DeleteEdge(e)
		e = t
	base = MakeEdge()
	first = e.origin
	base.origin = first
	base.destination = vertex
	Splice(base, e)
	base.fix_edge()
	while e.destination != first:
		e.fix_edge()
		base.fix_edge()
		base = Connect(e, base.Sym())
		e = base.Oprev()
	e = base.Oprev()
	e.fix_edge()
	# DO
	while True:
		t = e.Oprev()
		if (RightOf(t.destination, e) > 0.0) and Incircle(e.origin, t.destination, e.destination, vertex) > 0:
			Swap(e)
			e = t
		elif e.origin == first:
			return
		else:
			e = e.Onext().Lprev()
	#OD

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
	qedges += [quadedge]

	return quadedge.edges[0]

def draw_2D(triangle_list,alpha=0.1,colour_same = 1,thickness = 1):
    """
    The corresponding thing for 2D drawing
    """
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(8,8))
    for data in triangle_list:
        order = [0,1,2,0]
        cds = np.array([data[i] for i in order]).transpose()
        if colour_same == 1:
            plt.plot(cds[0],cds[1],alpha=alpha,color='black',linewidth=thickness)
        else:
            plt.plot(cds[0],cds[1],alpha=alpha,linewidth=thickness)
    plt.show()
    #draw_2D([[[0, 0], [1, 0], [0, 1]], [[0, 0], [1, 10], [10, 1]]], alpha=1)

filename = sys.argv[1]
#filename = "testfiles/spiral.node"
f = open(filename, "r")

vertices = f.read().split("\n")
vertices = [[float(i) for i in v.split()] for v in vertices]
numvertices, dim, numattributes, numBmarkers = vertices[0] 

dim = int(dim)
numvertices = int(numvertices)

vertices = vertices[1:numvertices+1]
for i in range(numvertices):
	vertices[i] = Vertex(vertices[i][1:], i+1)
f.close()

qedges = []

first = vertices[0]
second = vertices[1]
start = MakeEdge()
start.origin = first
start.destination = second
start.fix_edge()


for v in vertices[2:]:
	InsertSite(v)

f = open(filename[:len(filename)-5]+".ele", "a")
f.truncate(0)
lst = []
count = 0
for i in range(len(qedges)):
	e = qedges[i].edges[0]
	if not e.seen:
		count = count + 1
		e.seen = True
		e.Lnext().seen = True
		e.Lnext().Lnext().seen = True
		triangle = [e.origin.c, e.Lnext().origin.c, e.Lnext().Lnext().origin.c]
		f.write("{} {} {} {}\n".format(count, triangle[0], triangle[1], triangle[2]))
		lst += [[triangle[0], triangle[1], triangle[2]]]

#draw_2D(lst, alpha=1,colour_same=0)
draw_2D(lst, alpha=1)

f.close()





