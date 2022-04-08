// ¥∫ºæ—µ¡∑”™2£∫ I ∆Â≈Ã∏≤∏«Œ Ã‚ 
#include<bits/stdc++.h>
using namespace std;

int k, xx, yy, n, id=0, id2=0;
int new_id[1025*1025];
int aa[1030][1030];
int dx[4] = {0, 0, 1, 1}, dy[4] = {0, 1, 0, 1};

void solve(int k, int x, int y, int dir)
{
	int m = k / 2;
	int d = dir >= 0 ? dir : (xx >= x + m) * 2 + (yy >= y + m);
	if(k == 2)
	{
		++id;
		for(int i = 0; i < 4; i++)
		{
			if(d != i)
			{
				aa[x + dx[i]][y + dy[i]] = id;
			}
		}
	}
	else
	{
		for(int i = 0; i < 4; i++)
		{
			if(d != i)
			{
				solve(m, x + dx[i] * m, y + dy[i] * m, 3 - i);
			}					
		}
		solve(m, x + m / 2, y + m / 2, d);
		if(dir < 0)
		{
			solve(m, x + dx[d] * m, y + dy[d] * m, -1);
		}
	}	
} 
 
int main()
{
	ios::sync_with_stdio(false);
	
	cin>>k>>xx>>yy;
	n = 1<<k;
	solve(n, 1, 1, -1);
	for(int i=1; i<=n; i++)
	{
		for(int j=1; j<=n; j++)
		{
			if(aa[i][j]&&new_id[aa[i][j]]==0)
			{
				++id2;
				new_id[aa[i][j]] = id2;
			}
			cout<<new_id[aa[i][j]]<<" ";
			//cout<<aa[i][j]<<" ";
		}
		cout<<endl;
	}
	
	return 0;
}
