// ´óÂÒ¶· 6 £ºF ¿òÂìÒÏ 
#include<bits/stdc++.h>
using namespace std;

long long pminx, pmaxx, pminy, pmaxy, sminx, smaxx, sminy, smaxy;
long long n, xx, yy, ans1, ans2, ans;

int main()
{	
	cin>>n;
	for(int i=1; i<=n; i++)
	{
		cin>>xx>>yy;
		if(i == 1)
		{
			pminx = pmaxx = xx;
			pminy = pmaxy = yy;
			sminx = smaxx = yy + xx;
			sminy = smaxy = yy - xx;
		}
		else
		{
			if(pminx > xx) pminx = xx;
			if(pmaxx < xx) pmaxx = xx;
			if(pminy > yy) pminy = yy;
			if(pmaxy < yy) pmaxy = yy;
			if(sminx > yy + xx) sminx = yy + xx;
			if(smaxx < yy + xx) smaxx = yy + xx;
			if(sminy > yy - xx) sminy = yy - xx;
			if(smaxy < yy - xx) smaxy = yy - xx;
		}
	}
	ans1 = pmaxx-pminx > pmaxy-pminy ? (pmaxx-pminx) * (pmaxx-pminx) : (pmaxy-pminy) *(pmaxy-pminy);
	ans2 = smaxx-sminx > smaxy-sminy ? (smaxx-sminx) * (smaxx-sminx) / 2 : (smaxy-sminy) *(smaxy-sminy) / 2;
	
	ans = ans1 < ans2 ? ans1 : ans2;
	cout<<ans;
    return 0;
}
