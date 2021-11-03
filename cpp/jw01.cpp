#include<bits/stdc++.h>
using namespace std; 
int jose[100];

int main()
{
	int n, k, m, start;
	cin>>n>>k>>m;
	
	for(int i=1; i<=n; i++)
		jose[i] = i;
		
	start = k; 
	
	while(n>1) 
	{	/*
		if((start + m - 1)%n!=0)
		{
			start = (start + m - 1)%n;
		}
		else
		{
			start = n;
		}
		*/
		start = (start + m - 1)%n ? (start + m - 1)%n : n;

		cout<<n<<" : "<<jose[start]<<endl;
		
		n--;

		for(int i=start; i<=n; i++)
		{
			jose[i] = jose[i+1];
		}
	}
	cout<<n<<" : "<<jose[1]<<endl;
	return 0;
}
