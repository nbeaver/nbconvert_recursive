run :
	./nbconvert_recursive.py .

verbose:
	./nbconvert_recursive.py --verbose .

debug :
	./nbconvert_recursive.py --debug .

no-act :
	./nbconvert_recursive.py --no-act .

time :
	/usr/bin/time --verbose ./nbconvert_recursive.py .

clean :
	rm -f -- example.html
