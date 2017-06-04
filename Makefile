#NAME:Samantha Tran, Apurva Panse
#EMAIL: samantha.tran95@gmail.com
#ID: 804282884 504488023

default:
	gcc -o lab3b -g lab3b.c

clean:
	rm -r lab3b-504488023.tar.gz output.csv

dist:
	tar -zcvf lab3b-504488023.tar.gz README Makefile lab3b.c
