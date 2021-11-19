#include<bits/stdc++.h>
using namespace std;
int main()
{
	char a[100001];
	int b,c[100001]={0};
	cin.getline(a, sizeof(a));
	b=strlen(a);
	for(int i=0;i<b;i++)
	{
		for(int j=0;j<b;j++)
		{
			if(a[i]!=a[j])
				c[i]++;
		}
		if(c[i]==b-1)
		{
			cout<<a[i];
			return 0;
		}
	}
	cout<<"no";
	return 0;
}
