#include<bits/stdc++.h>
using namespace std;

int main()
{
	const long long aa=5e15;
    string s1;
    cin>>s1;

    long long k, sum=0, len, up;
    cin>>k;
	len = s1.length(); 
	for(int i=0; i<len; i++)
	{
		if(s1[i]=='1')
		{
			up = 1;
		}
		else
		{
			up =  pow(s1[i]-'0', aa);
			cout<<up<<endl;
		}
		if(k==1)
		{
			cout<<s1[0];
			break;
		}
		else
		{
			if(sum<k&&sum+up>=k)
			{
				cout<<s1[i];
				break;
			}
		}
	}

    return 0;
}
