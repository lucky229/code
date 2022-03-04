// ´óÂÒ¶· 6  £ºe ËÍÍâÂô 
#include<bits/stdc++.h>
using namespace std;
queue<int> pai; 
int main()
{
	int n, m, cnt=1;
	cin>>n;
	for(int i=1; i<=n; i++)
	{
		pai.push(i);
	}
	while(pai.size()!=0)
	{
		cout<<pai.front()<<" ";
		pai.pop();
		m = pai.front();
		pai.pop();
		pai.push(m);

	}
	
    return 0;
}
