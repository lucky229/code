// ´óÂÒ¶· 5  £ºf ÇÐÈ¦È¦ 
#include<bits/stdc++.h>
using namespace std;

long long t, n, nn, zs[20020], sum[20020]; 

int main()
{
	cin>>t;
	for(int i=1; i<=n; i++)
	{
		cin>>sz[i];
		sz[i+n] = sz[i];		
	}
	sum[1] = sz[1];
	nn = 2 * n;
	for(int i=2; i<nn; i++)
	{
		sum[i] = sum[i-1] + sz[i];
	}
	
	
    return 0;
}
