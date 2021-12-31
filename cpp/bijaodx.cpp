// ด๓ยาถท 6  ฃบe หออโย๔ 
#include<bits/stdc++.h>
using namespace std;

long long n, a[100010], all=0, ans; 

int main()
{
	cin>>n;
	int s = 0;
	for(int i=1; i<=n; i++)
	{
		cin>>a[i];
		all = all + abs(a[i] - s);
		s = a[i];
	}
	all = all + abs(a[n]);

	for(int i=1; i<=n; i++)
	{
		if(i==1)
		{
			ans = all - abs(a[i]) -abs(a[i+1] - a[i]) + abs(a[i+1]);
		}
		else if(i==n)
		{
			ans = all - abs(a[i] - a[i-1]) - abs(a[i]) + abs(a[i-1]);
		}
		else
		{
			ans = all - abs(a[i] - a[i-1]) - abs(a[i+1] - a[i]) + abs(a[i+1] - a[i-1]);
		}
		cout<<ans<<endl;
	}
	
    return 0;
}
