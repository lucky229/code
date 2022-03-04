#include<bits/stdc++.h>
using namespace std;
int n;
queue<int>b,c;
 
int main()
{
	scanf("%d", &n);
	int x = 1;
	for(int i=1;i<=n;i++)
	{
		printf("%d ", x);
		b.push(2 * x + 1);
		c.push(3 * x + 1);
		if(b.front()<c.front())
		{
			x = b.front();
			b.pop();
		}
		else
		{
			x = c.front();
			c.pop();
		}
		if(b.front() == c.front())
		{
			b.pop();
		}
	}
	
	return 0;
}
