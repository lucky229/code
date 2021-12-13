// 训练营 5 ：T 求一些和 
#include<bits/stdc++.h>
using namespace std;

int swh(int x)
{
	int ss=0;
	ss = x/10000 + x/1000%10 + x/100%10 + x/10%10 + x%10;
	
	return ss;
}

int main()
{
	int n, a, b, sum=0, s;
	cin>>n>>a>>b;
	for(int i=1; i<=n; i++)
	{
		s = swh(i);
		if(s>=a&&s<=b)
		{
			sum = sum + i;
		}
	}
	cout<<sum;
	
    return 0;
}
