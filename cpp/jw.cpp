#include<bits/stdc++.h>
using namespace std; 
int jose[100];

int main()
{
	int n, k, m, num, start;
	cin>>n>>k>>m;
	
	for(int i=1; i<=n; i++)
		jose[i] = 1;                      //�� 1-N ��� 
	
	start = k;                            //��һ�ο�ʼ��λ�� 
	num = 0; 
	while(num<n)               //���ֵ�������Ϊѭ�� 
	{
		int j = 0;
		while(j<m)
		{
			if(jose[start]!=0)            //��λ�õ�ֵ��Ϊ0ʱ 
			{
				j++;                      //�����һ 
				if(j==m)                  //������� m ���� 
				{
					num++;                //�ֵ��������� 1
					jose[start]=0;        //�ô���ֵ����Ϊ 0 
					cout<<num<<" : "<<start<<endl;    //����ô��ı�� 
				}
			}
			start++;                      //�ֶ�����Զ����� 
			if(start==n+1)
			{
				start = 1;                //����ֶ���ǳ��� n�� �Զ��� 1 ��ʼ 
			}
		}
	}
	return 0;
}
