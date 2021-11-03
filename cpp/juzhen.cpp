#include<bits/stdc++.h>
using namespace std;

int a[55][55];
int b[55][55];
int c[55][55];
//ÑµÁ·Óª 3 £º P¾ØÕóÏà³Ë 
int main()
{
	int m, w, n;
	cin>>m>>w>>n;
	
	for(int i=1; i<=m; i++)
	{
		for(int j=1; j<=w; j++)
		{
			cin>>a[i][j];
		}
	}
	
	for(int i=1; i<=w; i++)
	{
		for(int j=1; j<=n; j++)
		{
			cin>>b[i][j];
		}
	}
	
	for(int i=1; i<=m; i++)
	{
		for(int j=1; j<=n; j++)
		{
			c[i][j] = 0;
			for(int k=1; k<=w; k++)
				c[i][j] = c[i][j] + a[i][k] * b[k][j];
		}
	}
	
	for(int i=1; i<=m; i++)
	{
		for(int j=1; j<=n; j++)
		{
			cout<<c[i][j]<<" ";
		}
		cout<<endl;
	}
	
	return 0;
}
