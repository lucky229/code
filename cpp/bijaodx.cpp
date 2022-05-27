#include<bits/stdc++.h>
using namespace std;
int x,y,z;
int a[210],b[210],c[210];
int xx[210],xy[210];
int f[210][210];
bool d[210];
int main()
{
	scanf("%d%d%d",&x,&y,&z);
	for(int i=1;i<=x;i++)
	{
		scanf("%d",&a[i]);
	}
	for(int i=1;i<=y;i++)
	{
		scanf("%d",&b[i]);
	}
	for(int i=1;i<=z;i++)
	{
		scanf("%d",&c[i]);
	}
	for(int i=1;i<=x;i++)
	{
		for(int j=1;j<=y;j++)
		{
			for(int k=1;k<=z;k++)
			{
				if(a[i]==b[j]&&b[j]==c[k])
				{
					f[j][k]=f[j][k-1]+1;
				}
				else
				{
					f[j][k]=max(f[j][k],max(f[j][k-1],f[j-1][k]));
				} 
				cout<<i<<" -- "<<j<<" -- "<<k<<" : "<<f[j][k]<<endl;
			}				
		}
	}
	printf("%d",f[y][z]);
	return 0;
}
