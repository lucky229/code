#include<bits/stdc++.h>
using namespace std;
int main()
{
	char a[110];
	cin.getline(a, sizeof(a));
	int len=strlen(a);
	for(int i=0;i<len;i++)
	{
		if(islower(a[i]))
		{
			a[i] = toupper(a[i]);
		}
	}
	printf("%s", a);
	return 0;
}  
