#include "test.h"

void edgepartition1D_test()
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
		
		int ceilSqrtNumParts = (int)(sqrt(parts) + 1);
		long long mixingPrime = 1125899906842597L;
		numP = (llabs(src * mixingPrime)) % parts;
		
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

	cout << "edgepartition1D VRF is : " << VRF << endl;
	cout << "edgepartition1D vertices is : " << Graph.v.size() << endl;
	cout << "edgepartition1D edges is : " << Graph.e.size() << endl;
	for(int i = 0; i < parts; i++)
	{
		//cout << "partition " << i << " edges is " << Part[i].e.size() << "  vertices is " << Part[i].v.size() << endl;
	}
}