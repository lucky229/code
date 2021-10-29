#include<bits/stdc++.h>
#include<climits>
using namespace std; 

int main()
{
	int n, k, ans;
	cin>>n>>k;
	
	for(int m=1;m <= n; m++)
	{
		if(n%m==0)
		{
			ans = n/m + k*m;
			cout<<m<<endl;
		}
		if((ans/k)*(ans%k) == n)
			break;
	}

	cout<<ans; 

	return 0;
}
