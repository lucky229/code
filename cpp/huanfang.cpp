#include<bits/stdc++.h>
using namespace std;
//训练营 3 ： S神奇的幻方 
int a[40][40] = {0};

int main()
{
	int n, na, nb;
	cin>>n;
	
	na = 1;
	nb = n/2 + 1;
	
	a[na][nb] = 1;
	
	for(int i=2; i<=n*n; i++)
	{
		if(na == 1 && nb != n)
		{
			na = n;
			nb++;
		}
		else if(na != 1 && nb ==n)
		{
			na--;
			nb = 1;
		}
		else if(na == 1 && nb == n)
		{
			na++;
		}
		else if(na != 1 && nb != n)
		{
			if(a[na-1][nb+1]==0)
			{
				na--;
				nb++;
			}
			else
			{
				na++;
			}
		}
		a[na][nb] = i;
	}
	
	for(int i=1; i<=n; i++)
	{
		for(int j=1; j<=n; j++)
		{
			cout<<a[i][j]<<" ";
		}
		cout<<endl;
	}
	
	return 0;
}
