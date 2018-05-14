#include "test.h"

int main()
{
	srand((unsigned)time(NULL));
	cout << "Start testing..........................." << endl << endl;
	
	// cout << "random from graphx ans is .............." << endl << endl;
	// random_test();
	
	// cout << "canonicalrandom from graphx ans is ....." << endl << endl;
	// canonicalrandom_test();

	// cout << "edgepartition1D from graphx ans is ....." << endl << endl;
	// edgepartition1D_test();

	// cout << "edgepartition2D from graphx ans is ....." << endl << endl;
	// edgepartition2D_test();

	cout << "powergraph from graphx ans is .........." << endl << endl;
	powergraph_test();



	return 0;
}
