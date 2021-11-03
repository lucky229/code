#include<bits/stdc++.h>
using namespace std;
//训练营 3 ： a 数组价值 
int a[1000010];

int main()
{
	int n;
	cin>>n;
	long long sum=0, sum1=0, sum2=0, maxx=0;
	
	for(int i=1; i<=n; i++)
	{
		cin>>a[i];
		sum += a[i];
	}
	
	for(int i=1; i<=n; i++)
	{
		sum1 += a[i];
		sum2 += a[i] * a[i];
		if(sum2 * (sum - sum1) > maxx)
		{
			maxx = sum2 * (sum - sum1);
		}
	}
	
	cout<<maxx<<endl;
	
	return 0;
}
