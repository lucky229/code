#include<bits/stdc++.h>
using namespace std;

int n, m, x, y;
int f[30];
int main()
{
	scanf("%d%d%d%d", &n, &m, &x, &y);
	f[0] = 1;
	for(int i=0; i<=n; i++)
	{
		for(int j=0; j<=m; j++)
		{
			bool xy = (i==x&&j==y)||(i==x+1&&(j==y+2||j==y-2))||(i==x+2&&(j==y+1||j==y-1))||(i==x-1&&(j==y+2||j==y-2))||(i==x-2&&(j==y+1||j==y-1));
			if(!xy)
			{
				if(j!=0)
				{
					f[j] = f[j-1] + f[j];
				}				
			}
			else
			{
				f[j] = 0;
			}
			//cout<<i<<" -- "<<j<<"  :  "<<f[j]<<endl;
		}
	}
	printf("%d", f[m]);
	return 0;
}
