# $@ name of target
# $< name of first dependancy
# $^ names of all dependancies

CC       = g++ -Wall -g


all: exprtest

exprtest: exprtest.o driver.o parser.tab.o scanner.o
	${CC} -o $@ $^

exprtest.o: exprtest.cpp
	${CC} -c $<

driver.o: driver.cpp scanner.hpp driver.hpp parser.tab.hpp
	${CC} -c $<

parser.tab.o: parser.tab.cpp parser.tab.hpp expression.hpp scanner.hpp driver.hpp
	${CC} -c $<

scanner.o: scanner.cpp scanner.hpp parser.tab.hpp
	${CC} -c $<

parser.tab.hpp parser.tab.cpp: parser.ypp
	bison $^

scanner.cpp: scanner.ll scanner.hpp
	flex -t $< > $@

clean:
	rm -f *.o
	rm -f parser.tab*
	rm -f scanner.cpp
	rm -f exprtest
	rm -f *.hh
