struct edge
	{
		int id; /*{0,1,2,3}*/

		vertex Origin;
		vertex Destination;
		edge Next;
		data data;

		quadedge qedge;
	}

edge Rot (edge e)
{
	return e.qedge->edges[mod(id+1, 4)];
}
edge Rot_inv (edge)
{
	return e.qedge->edges[mod(id-1, 4)];
} 

// edge Flip (edge e) 
// {
// 	return quadedge->edges[]
// }

edge Sym (edge e)
{
	return Rot(Rot(e));
}

edge Onext (edge e)
{
	return e.Next;
}

edge Oprev (edge e)
{
	return Rot(Onext(Rot(e)));
}

edge Lnext (edge e)
{
	return Rot(Onext(Rot_inv(e)));
}

edge Lprev (edge e)
{
	return Sym(Onext(e));
}

edge Dprev (edge e)
{
	return Rot_inv(Onext(Rot_inv(e)));
}



