// ÑµÁ·Óª 5 £ºU ºÎÀÏ°å°ÚÌ¯ 
#include<bits/stdc++.h>
using namespace std;

int maxx(int x, int y, int z)
{
	int sum = max(x, max(y, z))>=0?max(x, max(y, z)):0;
	return sum;
}

int main()
{
	int n, a, b, c, sum=0;
	cin>>n;
	for(int i=1; i<=n; i++)
	{
		cin>>a>>b>>c;
		sum = sum + maxx(a, b, c);
	}
	if(sum>=n*10)
	{
		cout<<sum-n*10;
	}
	else
	{
		cout<<"Clever He";
	}
	
    return 0;
}
