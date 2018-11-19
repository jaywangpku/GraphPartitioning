#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <set>
#include <unordered_set>
#include <math.h>
#include <functional>
#include <algorithm>

using namespace std;

#define parts 4
#define file "/home/w/data/Wiki-Vote.txt"  //Wiki-Vote   mytest

struct edge{
	long src;
	long dst;
	bool operator<(const edge &e)const {
		if(this->src < e.src)
			return true;
		else if(this->src == e.src)
			return this->dst < e.dst;
		else
			return false;
	}
	bool operator==(const edge &e)const {
		if(this->src == e.src && this->dst == e.dst)
			return true;
		else
			return false;
	}
};

struct myHash4edge{
	size_t operator()(struct edge e) const
	{
		return static_cast<size_t>(e.src + e.dst);
	}
};

struct partition{
	unordered_set<struct edge, myHash4edge> e;
	unordered_set<long> v;
	vector<struct edge> vec_e;
	vector<long> vec_v;
	int partID;
};

struct graph{
	unordered_set<struct edge, myHash4edge> e;
	unordered_set<long> v;
	int numOfParts = parts;
};

void random_test();
void canonicalrandom_test();
void edgepartition1D_test();
void edgepartition2D_test();
void powergraph_test();
