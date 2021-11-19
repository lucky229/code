#include<bits/stdc++.h>
using namespace std;
// 训练营 4 ： I 单词长度 
int main()
{
    char a[1010];
    cin.getline(a, sizeof(a));
    int num=0, len=strlen(a);
    for(int i=0;i<len;i++)
    {
        if(i!=len-1)
        {
        	if(a[i] != ' ')
        	{
        		num++;
			}
			else
			{
				printf("%d,", num);
				num = 0;
			}
		}
		else
		{
			num++;
			printf("%d", num);
		}
    }
    printf("\n");
    return 0;
}
