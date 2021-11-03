#include<bits/stdc++.h>
using namespace std;

int main()
{
	int n;
	long long ans=0, naa=1, yaa=0;
	cin>>n;
	//无 a 的情况 
	for(int i=1; i<=n; i++)
	{
		naa*=2; 
	}
	ans += naa;
	
	int maxa;
	maxa = n%2 ? n/2+1 : n/2;

	if(n==1)
		yaa = 1;
	else
	{
		for(int i=1; i<=maxa; i++)
		{
			long long yaau=1, yaad=1, yaan=1;
			for(int k=1; k<=n-i; k++)
			{
				yaan *= 2;
			}
			for(int j=1; j<=i; j++)
			{
				yaau *= (n-j+1);
				yaad *= j;
			}
			yaa = yaa + (yaau/yaad)*yaan;
		}
	}
	
	cout<<naa+yaa<<endl;
	return 0;
}
