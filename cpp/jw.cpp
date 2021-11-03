#include<bits/stdc++.h>
using namespace std; 
int jose[100];

int main()
{
	int n, k, m, num, start;
	cin>>n>>k>>m;
	
	for(int i=1; i<=n; i++)
		jose[i] = 1;                      //从 1-N 标记 
	
	start = k;                            //第一次开始的位置 
	num = 0; 
	while(num<n)               //以轮到的人数为循环 
	{
		int j = 0;
		while(j<m)
		{
			if(jose[start]!=0)            //该位置的值不为0时 
			{
				j++;                      //向后数一 
				if(j==m)                  //如果数过 m 个人 
				{
					num++;                //轮到的人数加 1
					jose[start]=0;        //该处数值设置为 0 
					cout<<num<<" : "<<start<<endl;    //输出该处的标号 
				}
			}
			start++;                      //轮动标记自动增加 
			if(start==n+1)
			{
				start = 1;                //如果轮动标记超过 n， 自动从 1 开始 
			}
		}
	}
	return 0;
}
