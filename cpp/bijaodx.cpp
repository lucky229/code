#include<bits/stdc++.h>
using namespace std;
int r,n,c,cnt=0;
int x,xx,y,yy;
stack<int> s;
struct gg{
	int x,y,p,id;
}xa[200010];
bool check(int a,int b,int aa,int bb)
{
	if((a==0||a==r||b==0||b==c)&&(aa==0||aa==r||bb==0||bb==c))
	{
		return true;
	}
	else
	{
		return false;
	}
}
int chec(int x,int y)
{
	if(x==0)
	{
		return 1;
	}
	if(y==c)
	{
		return 2;
	}
	if(x==r)
	{
		return 3;
	}
	if(y==0)
	{
		return 4;
	}
}
bool cmp(gg a,gg b)
{
	if(a.p==b.p)
	{
		if(a.p==1)
		{
			return a.y<b.y;
		}
		if(a.p==2)
		{
			return a.x<b.x;
		}
		if(a.p==3)
		{
			return a.y>b.y;
		 } 
		if(a.p==4)
		{
			return a.x>b.x;
		}
	}
	else
	{
		return a.p<b.p;
	}
}
int main()
{
	ios::sync_with_stdio(false);
	cin>>r>>c>>n;
	for(int i=1;i<=n;i++)
	{
		cin>>x>>y>>xx>>yy;
		if(check(x,y,xx,yy)==true)
		{
			//cout<<i<<endl;
			cnt++;
			xa[cnt].x=x;
			xa[cnt].y=y;
			xa[cnt].id=i;
			//cout<<"cnt:"<<cnt<<" "<<xa[cnt].id<<endl;
			xa[cnt].p=chec(x,y);
			cnt++;
			xa[cnt].x=xx;
			xa[cnt].y=yy;
			xa[cnt].id=i;
			//cout<<"cnt:"<<cnt<<" "<<xa[cnt].id<<endl;
			xa[cnt].p=chec(xx,yy);
		}
	}
	//cout<<cnt; 
	sort(xa+1,xa+1+cnt,cmp);
	for(int i=1;i<=cnt;i++)
	{
		if(!s.empty()&&s.top()==xa[i].id)
		{
			s.pop();
		}
		else
		{
			s.push(xa[i].id);
		}
		//cout<<i<<": "<<xa[i].id<<endl;
	}
	if(s.empty())
	{
		cout<<"YES";
	}
	else
	{
		cout<<"NO";
	}
	return 0;
 }
