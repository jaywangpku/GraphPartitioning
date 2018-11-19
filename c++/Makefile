test : test.o random.o canonicalrandom.o edgepartition1D.o edgepartition2D.o powergraph.o
	g++ -std=c++11 -o test test.o random.o canonicalrandom.o edgepartition1D.o edgepartition2D.o powergraph.o

test.o : test.cpp test.h
	g++ -std=c++11 -c test.cpp

random.o : random.cpp test.h
	g++ -std=c++11 -c random.cpp

canonicalrandom.o : canonicalrandom.cpp test.h
	g++ -std=c++11 -c canonicalrandom.cpp

edgepartition1D.o : edgepartition1D.cpp test.h
	g++ -std=c++11 -c edgepartition1D.cpp

edgepartition2D.o : edgepartition2D.cpp test.h
	g++ -std=c++11 -c edgepartition2D.cpp

powergraph.o : powergraph.cpp test.h
	g++ -std=c++11 -c powergraph.cpp

clean:
	rm test *.o

run:
	make clean
	make
	./test

