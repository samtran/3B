#NAME:Samantha Tran, Apurva Panse
#EMAIL: samantha.tran95@gmail.com
#ID: 804282884 504488023
default:
	chmod u+x lab3b
	@echo "Program is built"

clean:
	rm -r lab3b-504488023.tar.gz 

dist:
	tar -zcvf lab3b-504488023.tar.gz README Makefile lab3b.py
