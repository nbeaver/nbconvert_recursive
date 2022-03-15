run :
	./nbconvert_recursive.py .

verbose:
	./nbconvert_recursive.py --verbose .

debug :
	./nbconvert_recursive.py --debug .

no-act :
	./nbconvert_recursive.py --no-act .

clean :
	rm -f -- example.html
