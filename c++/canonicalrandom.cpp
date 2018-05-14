#include "test.h"

void canonicalrandom_test()
{
	fstream fstrm;
	fstrm.open(file);
	long src, dst;

	unordered_set<long> vertices;
	unordered_set<struct edge, myHash4edge> edges;
	struct partition Part[parts];
	struct graph Graph;

	struct edge e;
	int numP = 0;
	while(fstrm >> src >> dst)
	{
		vertices.insert(src);
		vertices.insert(dst);
		e.src = src;
		e.dst = dst;
		edges.insert(e);
		
		hash<long> long_hash;
		if(src < dst)
			numP = long_hash(src) % parts;
		else
			numP = long_hash(dst) % parts;
		
		Part[numP].partID = numP; 
		Part[numP].e.insert(e);
		Part[numP].v.insert(src);
		Part[numP].v.insert(dst);

		Graph.e.insert(e);
		Graph.v.insert(src);
		Graph.v.insert(dst);
	}

	long allvertex = 0;
	for(int i = 0; i < parts; i++)
	{
		allvertex += Part[i].v.size();
	}
	double VRF = allvertex/1.0/Graph.v.size();

	cout << "canonicalrandom VRF is : " << VRF << endl;
	cout << "canonicalrandom vertices is : " << Graph.v.size() << endl;
	cout << "canonicalrandom edges is : " << Graph.e.size() << endl;
	for(int i = 0; i < parts; i++)
	{
		//cout << "partition " << i << " edges is " << Part[i].e.size() << "  vertices is " << Part[i].v.size() << endl;
	}
}