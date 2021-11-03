#include<bits/stdc++.h>
using namespace std;
// ÑµÁ·Óª 3 £º Z Æ»¹û²ÉÕª 
int a[100010]; 

int main()
{
	long long n, m;
	cin>>n>>m;
	int ans=0, wei=0;

	for(int i=1; i<=n; i++)
	{
		cin>>a[i]; 
	}

	for(int i=1; i<=n; i++)
	{
		if(a[i]>m)
			wei = 0;
		else if(a[i] == m)
		{
			ans ++;
			wei = 0;
		}			
		else
		{
			wei += a[i];
			if(wei>m)
				wei = 0;
			else if(wei == m)
				{
					ans ++;
					wei =0;
				}
		}			
	}
	
	cout<<ans<<endl;
	
	return 0;
}
