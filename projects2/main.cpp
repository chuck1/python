#include <stdio.h>

#define N (100000)

int primes[N];

int check(int c, int i)
{
	for(int j = 0; j < c; j++) {
		int p = primes[j];
		int r = i % p;
		//printf("p=%i i=%i r=%i\n", p, i, r);
		if(r == 0) {
			return 0;
		}
	}
	return 1;
}

int main()
{

	primes[0] = 2;

	// index into primes array
	int c = 1;
	// current number to check
	int i = 2;

	while(c < N) {
		if(check(c, i)) {
			primes[c] = i;
			c++;
			printf("%8i\n", i);
		}
		i++;
	}
}

