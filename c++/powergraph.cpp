#include "test.h"

void powergraph_test()
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
		unordered_set<long>::iterator src_iter, dst_iter;
		src_iter = vertices.find(src);
		dst_iter = vertices.find(dst);

		// 两个点都没有被分配的情况
		if(src_iter == vertices.end() && dst_iter == vertices.end())
		{
			//cout << "neither" << endl;
			long size = 0;
			for(int i = 0; i < parts; i++)
			{
				if(size >= Part[i].e.size())
				{
					size = Part[i].e.size();
					numP = i;
				}
			}
		}
		// 一个点被分配，一个点没有被分配的情况
		else if( (src_iter == vertices.end() && dst_iter != vertices.end())|| 
				 (src_iter != vertices.end() && dst_iter == vertices.end())   )
		{
			//cout << "only one" << endl;
			if(dst_iter != vertices.end())
			{
				long size = 0;
				for(int i = 0; i < parts; i++)
				{
					int dstNum = count(Part[i].vec_v.begin(), Part[i].vec_v.end(), dst);
					if(size <= dstNum)
					{
						size = dstNum;
						numP = i;
					}
				}
			}
			else if(src_iter != vertices.end())
			{
				long size = 0;
				for(int i = 0; i < parts; i++)
				{
					int srcNum = count(Part[i].vec_v.begin(), Part[i].vec_v.end(), src);
					if(size <= srcNum)
					{
						size = srcNum;
						numP = i;
					}
				}
			}
		}
		// 两个点都被分配的情况
		else
		{
			//cout << "both" << endl;
			long srcA[parts], dstA[parts], allA[parts], coverA[parts];  // 用于记录两个点存在的分区的num
			bool intersect = false;
			for(int i = 0; i < parts; i++)
			{
				srcA[i] = 0;
				dstA[i] = 0;
				allA[i] = 0;
				coverA[i] = 0;
			}
			for(int i = 0; i < parts; i++)
			{
				src_iter = Part[i].v.find(src);
				dst_iter = Part[i].v.find(dst);
				if(src_iter != Part[i].v.end())
				{
					srcA[i] = count(Part[i].vec_v.begin(), Part[i].vec_v.end(), src);
				}
				if(dst_iter != Part[i].v.end())
				{
					dstA[i] = count(Part[i].vec_v.begin(), Part[i].vec_v.end(), dst);
				}
				if((srcA[i] >= 1) && (dstA[i] >= 1))
				{
					allA[i] = srcA[i] + dstA[i];
					intersect = true;
				}
				if((srcA[i] >= 1) || (dstA[i] >= 1))
				{
					coverA[i] = srcA[i] + dstA[i];
				}
				cout << endl << "src " << src << "dst " << dst << endl;
				cout << allA[i] << " " << srcA[i] << " " << dstA[i] << " " << coverA[i] << endl;
			}
		
			if(intersect)
			{
				long size = 0;
				for(int i = 0; i < parts; i++)
				{
					if(size <= allA[i])
					{
						size = allA[i];
						numP = i;
					}
				}
			}
			else
			{
				long size = 0;
				for(int i = 0; i < parts; i++)
				{
					if(size <= coverA[i])
					{
						size = coverA[i];
						numP = i;
					}
				}
			}
		}
		cout << "numP " << numP << endl;
		static int j = 0;
		j++;
		if(j == 30)
			break;

		vertices.insert(src);
		vertices.insert(dst);
		e.src = src;
		e.dst = dst;
		edges.insert(e);

		Part[numP].partID = numP; 
		Part[numP].e.insert(e);
		Part[numP].v.insert(src);
		Part[numP].v.insert(dst);
		Part[numP].vec_e.push_back(e);
		Part[numP].vec_v.push_back(src);
		Part[numP].vec_v.push_back(dst);

		vector<long>::iterator iter;
		//unordered_set<struct edge>::iterator eiter;
		cout << endl;
		for(int i = 0; i < parts; i++)
		{
			cout << "part " << i << " : ";
			for(iter = Part[i].vec_v.begin(); iter != Part[i].vec_v.end(); iter++)
			{
				cout << *iter << " ";
			}
			cout << endl;
		}

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

	cout << "powergraph VRF is : " << VRF << endl;
	cout << "powergraph vertices is : " << Graph.v.size() << endl;
	cout << "powergraph edges is : " << Graph.e.size() << endl;
	for(int i = 0; i < parts; i++)
	{
		cout << "partition " << i << " edges is " << Part[i].e.size() << "  vertices is " << Part[i].v.size() << endl;
	}
}