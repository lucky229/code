#include <bits/stdc++.h>
#include <windows.h>
#define KEY_DOWN(VK_NONAME) ((GetAsyncKeyState(VK_NONAME) & 0x8000) ? 1:0)
#define N 10005
using namespace std;
struct plane//�ɻ�
{
	int pos_x,pos_y,size,vis;//pos_x,pos_y��λ�ã�size�Ǵ�С��vis�Ǽ�¼�Ƿ����
}plane[N+5],player;
struct bullet//�ӵ�
{
	int pos_x,pos_y,vis;//pos_x,pos_y��λ�ã�vis���Ƿ����
}bullet[N+5];
char game_map[50][50],plane_size[10][10][10];
//game_map�ǵ�ͼ(�ĵ�ͼ��С���������
//���򳬹���С�����ҵ���c++�и�������������
//�������к��񲻻�RE���ǻ�Ѻ�������Ŀռ�ռ�ˣ��е��������������ֱ��RE
//plane_size��ɻ���״
int dx[4]={0,0,-1,1},dy[4]={-1,1,0,0};
int store,map_size,n,game_time,last_attack,game_score,attack_average=20;
void print();//����Ļ�����
void start();//��ʼ��
void run();//��Ҫ�����к���
void check_die();//�ж��������
void player_cover();//��ͼ����Ҹ���
void run_plane();//�ƶ��л������ж�����
void create_plane();//���ɵл�
int check_direction();//�����Ұ���
void game_end();//��Ϸ����
void player_attack();//��ҹ���
void map_cover(int x);//��ͼ����
int main()//������
{
	start();
	run();
	return 0;
}
int check_direction()//�����Ұ���
{
	if (KEY_DOWN(VK_LEFT))
	{
		while (KEY_DOWN(VK_LEFT));
		return 0;//��
	}
	if (KEY_DOWN(VK_RIGHT))
	{
		while (KEY_DOWN(VK_RIGHT));
		return 1;//��
	}
	if (KEY_DOWN(VK_UP))
	{
		while (KEY_DOWN(VK_UP));
		return 2;//��
	}
	if (KEY_DOWN(VK_DOWN))
	{
		while (KEY_DOWN(VK_DOWN));
		return 3;//��
	}
	if (KEY_DOWN('A'))
	{
		while (KEY_DOWN('A'));
		return 0;//��
	}
	if (KEY_DOWN('D'))
	{
		while (KEY_DOWN('D'));
		return 1;//��
	}
	if (KEY_DOWN('W'))
	{
		while (KEY_DOWN('W'));
		return 2;//��
	}
	if (KEY_DOWN('S'))
	{
		while (KEY_DOWN('S'));
		return 3;//��
	}
	return 4;//û�а���
}
void map_cover(int x)//��ͼ����
{
	int sz=plane[x].size,pos_x=plane[x].pos_x,pos_y=plane[x].pos_y;
	for (int i=1;i<=sz+1;i++)
	{
		for (int j=1;j<=sz*2+1;j++)
		{
			if (plane_size[sz][i][j]!=' ' && pos_x+j-sz-1>1 && pos_y+i-1>1)
			{
				if (game_map[pos_x+j-sz-1][pos_y+i-1]=='|')
				{//�ж��л�����
					game_score++;
					plane[x].vis=0;
					return;
				}
			}
		}
	}
	for (int i=1;i<=sz+1;i++)
	{
		for (int j=1;j<=sz*2+1;j++)
		{
			if (plane_size[sz][i][j]!=' ' && pos_x+j-sz-1>1 && pos_y+i-1>1)
			{//if���ж��Ƿ�Ҫ���Ǻ��Ƿ���һ�����ڱ߿�
				game_map[pos_x+j-sz-1][pos_y+i-1]='.';
			}
		}
	}
}
void game_end()//��Ϸ����
{
	cout<<"game_over\n�س��˳�\n";
	while (1)
	{
		if (KEY_DOWN(VK_RETURN)) exit(0);//�˳�����
	}
}
int game_life=1;
void check_die()//�ж�����Ƿ���л���ײ
{//����дѭ��������ʡ��
	if (game_map[player.pos_x][player.pos_y]=='.') game_life=0;
	if (game_map[player.pos_x-1][player.pos_y]=='.') game_life=0;
	if (game_map[player.pos_x+1][player.pos_y]=='.') game_life=0;
	if (game_map[player.pos_x][player.pos_y-1]=='.') game_life=0;
}
void player_cover()//��Ҹ���
{//����дѭ��������ʡ��
	game_map[player.pos_x][player.pos_y]='*';
	game_map[player.pos_x-1][player.pos_y]='*';
	game_map[player.pos_x+1][player.pos_y]='*';
	game_map[player.pos_x][player.pos_y-1]='*';
}
void print()//�������Ļ��
{
	system("cls");//��տ���̨
	for (int i=1;i<=map_size;i++)
	{
		for (int j=1;j<=map_size;j++) game_map[i][j]=' ';
	}//��ͼ���
	for (int i=1;i<N;i++)
	{
		if (bullet[i].vis)
		{
			int xx=bullet[i].pos_x,yy=bullet[i].pos_y;
			for (int j=0;j<4;j++) game_map[xx][yy+j]='|';
		}
	}//�ӵ�����
	for (int i=1;i<N;i++)
	{
		if (plane[i].vis)
		{
			map_cover(i);//���ǵл�
		}
	}
	check_die();
	player_cover();
	for (int i=1;i<=map_size;i++)
	{
		game_map[i][1]=game_map[i][map_size]=game_map[1][i]=game_map[map_size][i]='#';
	}//����߿�
	cout<<"score:"<<game_score<<"   time:"<<game_time<<"   attack space:"<<(5+max(0,20-attack_average))<<endl;
	//�������
	for (int j=1;j<=map_size;j++)
	{
		for (int i=1;i<=map_size;i++)
		{
			cout<<game_map[i][j];
		}
		cout<<endl;
	}//�ѵ�ͼ���������̨
	if (game_life==0) game_end();
}
void start()//��ʼ��
{
	store=0;//������ʼ��
	last_attack=0;//��һ�ι���
	game_time=0;//��Ϸ����֡��
	
	map_size=21;//��ͼ��С�������޸ģ��������˸�������������С
	
	player.pos_x=10;//��ҳ�ʼ��λ��
	player.pos_y=20;
	player.size=1;
	
	memset(plane_size,' ',sizeof(plane_size));
	for (int i=1;i<=3;i++) plane_size[1][1][i]='.';
	plane_size[1][2][2]='.';//�л�ģ�ͣ���СΪ1��
	
	for (int i=1;i<=5;i++) plane_size[2][1][i]='.';
	for (int i=1;i<=3;i++) plane_size[2][2][i+1]='.';
	for (int i=1;i<=1;i++) plane_size[2][3][i+2]='.';//�л�ģ�ͣ���СΪ2��
}
void run_plane()//�л��ƶ�
{
	for (int i=1;i<N;i++)
	{
		if (plane[i].vis)
		{
			plane[i].pos_y++;
			if (plane[i].pos_y>map_size) plane[i].vis=0;//�ж�����
		}
	}
}
void create_plane()//������ɷɻ�
{
	int cnt=0;
	for (int i=1;i<N;i++)
	{
		if (!plane[i].vis)//�ж��Ƿ�ʹ��
		{
			plane[i].size=rand()%2+1;
			plane[i].pos_y=2;
			plane[i].pos_x=rand()%(map_size-3-plane[i].size)+2;
			//��ֹ�еķɻ���һ�����ڱ߽�
			plane[i].vis=1;
			cnt++;
			if (cnt>=game_time/200+1) return;//�ﵽ�����˳�
		}
	}
}
void player_move()//����ƶ�
{
	int k=check_direction();
	int xx=player.pos_x+dy[k];
	int yy=player.pos_y+dx[k];
	if (k==4) return;
	if (xx>2 && xx<map_size-1 && yy>2 && yy<map_size)//�ж��Ƿ����ƶ�
	{
		player.pos_x=xx;
		player.pos_y=yy;
	}
}
void player_attack()//��ҹ���
{
	if (KEY_DOWN(VK_SPACE))//���ո񰴼�
	{
		if (game_time-last_attack>=(5+max(0,20-attack_average)))//������
		{
			attack_average=(attack_average*3+(game_time-last_attack))/4;
			last_attack=game_time;
			for (int i=1;i<N;i++)
			{
				if (!bullet[i].vis)
				{
					bullet[i].vis=1;
					bullet[i].pos_x=player.pos_x;
					bullet[i].pos_y=player.pos_y;
					return;
				}
			}
		}
	}
}
void run_bullet()//�ƶ��ӵ�
{
	for (int i=1;i<N;i++)
	{
		if (bullet[i].vis)
		{
			bullet[i].pos_y-=3;
			if (bullet[i].pos_y<0) bullet[i].vis=0;
		}
	}
}
void run()//���к���
{
	while (1)
	{
		game_time++;//game_time�Ǽ�¼��Ϸ֡��
		run_plane();//�л��ƶ�
		if (rand()%(game_time/200+2))
		{
			if (rand()%2) create_plane();
		}
		if (game_time%20==0) game_score++;//ÿ20֡��һ��
		player_move();//����ƶ�
		player_attack();//��ҹ���
		run_bullet();//�ӵ��ƶ�
		print();//���������̨
//		system("pause");
		Sleep(100);
	}
}

