// ´óÂÒ¶· 4  £ºe µãÀ¯Öò 
#include<bits/stdc++.h>
using namespace std;

long long n, k, lz[100010]; 

int main()
{
	cin>>n>>k;
	for(int i=1; i<=n; i++)
	{
		cin>>lz[i];
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
