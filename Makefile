#NAME:
#EMAIL:
#ID:

default:
	gcc -o lab3b -g lab3b.c

clean:
	rm -r lab3b-504488023.tar.gz output.csv

dist:
	tar -zcvf lab3a-504488023.tar.gz README Makefile lab3b.c
