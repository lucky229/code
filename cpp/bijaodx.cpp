// 训练营 5 ：o 分解质因数 
#include<bits/stdc++.h>
using namespace std;

bool zs(int x)
{
	for(int i=2; i<x; i++)
	{
		if(x%i==0)
		{
			return false;
		}
	}
	return true;
}
bool ys(int x, int y)
{
	if(y%x==0)
	{
		return true;
	}
	else
	{
		return false;
	}
}

int main()
{
	int a[10010], n, b;
	cin>>n;
	for(int i=1; i<=n; i++)
	{
		cin>>b;
		a[i] = b;
	}
	for(int i=1;i<=n; i++)
	{
		for(int j=2; j<a[i]; j++)
		{
			if(zs(j)&&ys(j, a[i]))
				cout<<j<<" ";
		}
		cout<<endl;
	}
	
    return 0;
}
