#include<bits/stdc++.h>
using namespace std;
long long y[110];
long long ys(int a)
{
	for(int i=1;i<=a;i++)
	{
		if(a%i==0)
		{
			cout<<i<<" ";
		}
	}
	return 0;
}
int main()
{
	long long x;
	cin>>x;
	for(int i=0;i<x;i++)
	{
		cin>>y[i];
	}
	for(int i=0;i<x;i++)
	{
		ys(y[i]);
		cout<<endl;
	}
	return 0;
}
