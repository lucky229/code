#include<bits/stdc++.h>
using namespace std;
int main()
{
	string a, b, c, d, e;
	a=b=c=d=e="No Data";
	int n;
	cin>>n;
	
	for(int i=0;i<n;i++)
	{
		string s;
		cin>>s;
		if(s=="0"||s=="1")
		{
			a = s;
		}
		else if(s.size()==1&&(s[0]<'0'||s[0]>'9'))
		{
			d = s;
		}
		else
		{
			int idot=0, istr=0;
			int slen = s.size();
			for(int b=0; b< slen; b++)
			{
				if(s[b]=='.') idot++;
				else if(s[0]<'0'||s[0]>'9') istr=1;
			}
			if(idot==0&&istr==0) b=s;
			else if(idot==1&&istr==0) c=s;
			else e=s;
		}
		return 0;
	}
}
