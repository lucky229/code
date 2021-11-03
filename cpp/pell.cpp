#include<bits/stdc++.h>
using namespace std;
// ÑµÁ·Óª 3 £ºT pellÊýÁÐ 
long long p[20010];

int main()
{
	int t;
	int tz[110];
	cin>>t;
	for(int i=1; i<=t; i++)
	{
		cin>>tz[i];
	}
	
	p[1] = 1;
	p[2] = 2;
	for(int i=3; i<=20001; i++)
	{
		p[i] = 2 * p[i-1] + p[i-2];
	}
	
	for(int i=1; i<=t; i++)
	{
		cout<<p[tz[i]]%32767<<endl;
	}
	return 0;
}
