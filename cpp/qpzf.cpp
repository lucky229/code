// ÑµÁ·Óª 5 £ºU ºÎÀÏ°å°ÚÌ¯ 2
#include<bits/stdc++.h>
using namespace std;

bool zs(int x)
{
	for(int i=2; i<x; i++)
	{
		if(x%i==0)
		{
			return false;
		}
	}
	return true;
}
int maxx(int k)
{
	int a[60], max1=0, max2=0, zs1=0, zs2=0, sum1, sum2, sum, b=0, cha;
	for(int i=0; i<k; i++) cin>>a[i];
	
	for(int i=0; i<k; i++)
	{
		for(int j=i; j<k; j++)
		{
			if(a[i]<a[j])
			{
				cha = a[i];
				a[i] = a[j];
				a[j] = cha;	
			} 
		}
		
	}
	for(int i=0; i<k; i++)
	{
		
	}
	cout<<a[i]<<endl;
	return sum;
}

int main()
{
	int n, a[6], sum=0;
	cin>>n;
	for(int i=1; i<=n; i++)
	{
		cin>>a>>b>>c>>d>>e;
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
