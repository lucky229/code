// ÍØÕ¹2  £ºe À¬»øÏİÚå 
#include<bits/stdc++.h>
using namespace std;
struct cow
{
	int t, f, h;
}a[110];

bool cmp(cow a, cow b)
{
	return a.t < b.t;
}

int depth, n;
int dp[110];

int main()
{
	cin>>depth>>n;
	for(int i=1; i<=n; i++)
	{
		cin>>a[i].t>>a[i].f>>a[i].h;
	}
	sort(a+1, a+n+1, cmp);
	dp[0] = 10;
	for(int i=1; i<=n; i++)
	{
		for(int j=depth; j>=0; j--)
		{
			if(dp[j] >= a[i].t)
			{
				if(a[i].h + j >= depth)
				{
					cout<<a[i].t<<endl;
					return 0;
				}
				else
				{
					dp[j+a[i].h] = max(dp[j+a[i].h], dp[j]);
					dp[j] += a[i].f;
				}
			}
		}
	}
	
	cout<<dp[0]<<endl;
	
    return 0;
}
