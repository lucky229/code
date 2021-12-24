// ´óÂÒ¶· 5 £ºE ¹ì¼£ÓÎÏ· 
#include<bits/stdc++.h>
using namespace std;

bool yx(int t, int x1, int y1, int x2, int y2)
{
	int tt;
	tt = abs(x1 - x2) + abs(y1 - y2);
	if((tt == t) || ((tt < t) && (t-tt)%2==0))
	{
		return true;
	}
	else
	{
		return false;
	}
}

int main()
{
	int n, t, x, y, t0 = 0, x0 = 0, y0 = 0;
	bool ans; 
	cin>>n;
	for(int i=1; i<=n; i++)
	{
		cin>>t>>x>>y;
		ans = yx(t-t0, x0, y0, x, y);
		if(ans==false)
		{
			cout<<"No";
			return 0;
		}
		t0 = t;
		x0 = x;
		y0 = y;
	}
	cout<<"Yes";
	
    return 0;
}
