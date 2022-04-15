// 2022ÄÏÓå´º¼¾ÑµÁ·Óª 3 £º B ×·Å£ 
#include<bits/stdc++.h>
#define max_n 100010
using namespace std;
int n,k;
int tt[max_n];

int bfs(int n, int k)
{
	if(n == k)
	{
		return 0;
	}
	
	queue<int> q;
	q.push(n);
	while(!q.empty())
	{
		int a=q.front();
		q.pop();
		int b[3]={a+1, a-1, 2*a};
		for(int i=0;i<3;i++)
		{
			//bool ax = a <= max(k*4/3,n) && a >= min(k*4/3,n) && tt[b[i]] == 0;
			//cout<<"a and ax : "<<a<<" and "<<ax<<endl;
			if(a <= max(k*4/3,n) && a >= min(k*4/3,n) && tt[b[i]] == 0)
			{
				q.push(b[i]);
				tt[b[i]] = tt[a] + 1;
				cout<<"b["<<i<<"] "<<"  tt :  "<<b[i]<<"  "<<tt[b[i]]<<endl; 
			}
		}
	}
	return tt[k];
}
int main()
{
	ios::sync_with_stdio(false);
	cin>>n>>k;
	cout<<bfs(n, k);
	return 0;
}
