// ÍØÕ¹2  £ºe À¬»øÏİÚå 
#include<bits/stdc++.h>
using namespace std;

int a[1024][1024];

void solve(int k, int x, int y, int v)
{
	if(k==0)
	{
		a[x][y] = v;
	}
	else
	{
		int m = 1<<k-1;
		solve(k-1, x, y, v);
		solve(k-1, x, y+m, v+m);
		solve(k-1, x+m, y, v+m);
		solve(k-1, x+m, y+m, v);
	}
 } 

int main()
{
	int n, k;
	scanf("%d", &k);
	n = 1<<k;
	
	solve(k, 1, 1, 1);
	
	for(int i=1; i<=n; i++)
	{
		for(int j=1; j<=n; j++)
		{
			printf("%d ", a[i][j]);
		}
		printf("\n");
	}
	
    return 0;
}
