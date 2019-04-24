struct quadedge
{
	edge edges[4]; /*non-dual*/
}

quadedge initQE(quadedge *q)
{
	q->edges[0].index = 0;
	q->edges[1].index = 1;
	q->edges[2].index = 2;
	q->edges[3].index = 3;
}

e InsertSite(vertex)