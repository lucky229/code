#include<bits/stdc++.h> 
using namespace std;
int n;
struct gg{
	int x;
	int y;
}a[510];
bool cmp(gg a,gg b)
{
	return a.x>b.x;
}
int main()
{
	cin>>n;
	for(int i=1;i<=n;i++)
	{
		cin>>a[i].x>>a[i].y;
	}
	sort(a+1,a+1+n,cmp);
	for(int i=1;i<=n;i++)
	{
		cout<<a[i].x<<" "<<a[i].y<<endl;
	}
}
