#include<bits/stdc++.h>
using namespace std;
int main()
{
	string a;
	scanf("%s", a);
	int len=a.length();
	for(int i=0;i<len;i++)
	{
		if(islower(a[i]))
		{
			a[i]=toupper(a[i]);
		}
	}
	printf("%s", a);
	return 0;
}  
