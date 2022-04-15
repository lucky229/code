#include<bits/stdc++.h>
using namespace std;
int n,k;
struct gg{
	int a,step;
	gg(int a_,int step_)
	{
		a=a_;
		step=step_;
	}
};
int bfs(int x0)
{
	queue<gg> q;
	q.push(gg(x0,0));
	while(!q.empty())
	{
		gg a=q.front();
		q.pop();
		int b[3]={a.a+1,a.a-1,2*a.a};
		for(int i=0;i<3;i++)
		{
			gg bb(b[i],a.step+1);
			if(bb.a<=max(k*4/3,n)&&bb.a>=min(k*4/3,n))
			{
				if(bb.a==k)
				{
					return bb.step;
				}
				else
				{
					q.push(bb); 
				}
			}
		}
	}
	return -1;
}
int main()
{
	ios::sync_with_stdio(false);
	cin>>n>>k;
	cout<<bfs(n);
	return 0;
}
