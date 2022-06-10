#include<bits/stdc++.h>
using namespace std;
long long n,ans=LLONG_MAX,minn;
long long a[5010],sum[5010]; 
long long f[5010][5010];
int main()
{
	scanf("%lld",&n);
	for(long long i=1;i<=n;i++)
	{
		scanf("%lld",&a[i]);
		sum[i]=sum[i-1]+a[i];
	}
	for(int j=1;j<=n;j++)
	{
		for(int i=1;i+j<=1+n;i++)
		{
			if(j==1)
			{
				f[i][j]=0;
			}
			else
			{
				for(int k=1;k<j;k++)
				{
					if(k==1)
					{
						minn=LLONG_MAX;
						//cout<<")(*";
					}
					//minn=min(minn,f[i][i+k-1]+f[i+k][j+i-1]);
					minn=min(minn,f[i][k]+f[i+k][j-k]);
			//cout<<f[i][i+k-1]+f[i+k][j+i-1]<<endl;

				}
				f[i][j]=sum[i+j-1]-sum[i-1]+minn;
			}
			cout<<f[i][j]<<" ";
		} 
		cout<<endl;
	}
	ans=min(ans,f[1][n]);
	cout<<f[1][n];
	return 0;
}
