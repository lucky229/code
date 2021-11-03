#include<bits/stdc++.h>
using namespace std;

int main()
{
	int n;
	long long ans=0, aa=1;
	cin>>n;
	//无 a 的情况 
	for(int i=1; i<=n; i++)
	{
		aa*=2; 
	}
	ans += aa;
	
	return 0;
}
