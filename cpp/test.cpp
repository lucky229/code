#include<bits/stdc++.h>
using namespace std; 

long long fac(int n)
{
	static long long f[30] = {1, 1};
	return f[n] ? f[n] : (f[n] = n * fac(n-1));	
} 
int main()
{
	cout<<fac(20);
	
	return 0;
}
