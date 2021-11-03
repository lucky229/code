#include <bits/stdc++.h>
#include <windows.h>
#define KEY_DOWN(VK_NONAME) ((GetAsyncKeyState(VK_NONAME) & 0x8000) ? 1:0)
#define N 10005
using namespace std;
struct plane//飞机
{
	int pos_x,pos_y,size,vis;//pos_x,pos_y是位置，size是大小，vis是记录是否存在
}plane[N+5],player;
struct bullet//子弹
{
	int pos_x,pos_y,vis;//pos_x,pos_y是位置，vis是是否存在
}bullet[N+5];
char game_map[50][50],plane_size[10][10][10];
//game_map是地图(改地图大小别忘改这里）
//否则超过大小会程序挂掉，c++有个很神奇的溢出，
//本机运行好像不会RE但是会把后面数组的空间占了，有的评测机上这样会直接RE
//plane_size存飞机形状
int dx[4]={0,0,-1,1},dy[4]={-1,1,0,0};
int store,map_size,n,game_time,last_attack,game_score,attack_average=20;
void print();//在屏幕上输出
void start();//初始化
void run();//主要的运行函数
void check_die();//判定玩家死亡
void player_cover();//地图上玩家覆盖
void run_plane();//移动敌机，并判定出界
void create_plane();//生成敌机
int check_direction();//检测玩家按键
void game_end();//游戏结束
void player_attack();//玩家攻击
void map_cover(int x);//地图覆盖
int main()//主函数
{
	start();
	run();
	return 0;
}
int check_direction()//检测玩家按键
{
	if (KEY_DOWN(VK_LEFT))
	{
		while (KEY_DOWN(VK_LEFT));
		return 0;//左
	}
	if (KEY_DOWN(VK_RIGHT))
	{
		while (KEY_DOWN(VK_RIGHT));
		return 1;//右
	}
	if (KEY_DOWN(VK_UP))
	{
		while (KEY_DOWN(VK_UP));
		return 2;//上
	}
	if (KEY_DOWN(VK_DOWN))
	{
		while (KEY_DOWN(VK_DOWN));
		return 3;//下
	}
	if (KEY_DOWN('A'))
	{
		while (KEY_DOWN('A'));
		return 0;//左
	}
	if (KEY_DOWN('D'))
	{
		while (KEY_DOWN('D'));
		return 1;//右
	}
	if (KEY_DOWN('W'))
	{
		while (KEY_DOWN('W'));
		return 2;//上
	}
	if (KEY_DOWN('S'))
	{
		while (KEY_DOWN('S'));
		return 3;//下
	}
	return 4;//没有按键
}
void map_cover(int x)//地图覆盖
{
	int sz=plane[x].size,pos_x=plane[x].pos_x,pos_y=plane[x].pos_y;
	for (int i=1;i<=sz+1;i++)
	{
		for (int j=1;j<=sz*2+1;j++)
		{
			if (plane_size[sz][i][j]!=' ' && pos_x+j-sz-1>1 && pos_y+i-1>1)
			{
				if (game_map[pos_x+j-sz-1][pos_y+i-1]=='|')
				{//判定敌机死亡
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
			{//if是判断是否要覆盖和是否有一部分在边框
				game_map[pos_x+j-sz-1][pos_y+i-1]='.';
			}
		}
	}
}
void game_end()//游戏结束
{
	cout<<"game_over\n回车退出\n";
	while (1)
	{
		if (KEY_DOWN(VK_RETURN)) exit(0);//退出程序
	}
}
int game_life=1;
void check_die()//判断玩家是否与敌机相撞
{//懒得写循环，这样省事
	if (game_map[player.pos_x][player.pos_y]=='.') game_life=0;
	if (game_map[player.pos_x-1][player.pos_y]=='.') game_life=0;
	if (game_map[player.pos_x+1][player.pos_y]=='.') game_life=0;
	if (game_map[player.pos_x][player.pos_y-1]=='.') game_life=0;
}
void player_cover()//玩家覆盖
{//懒得写循环，这样省事
	game_map[player.pos_x][player.pos_y]='*';
	game_map[player.pos_x-1][player.pos_y]='*';
	game_map[player.pos_x+1][player.pos_y]='*';
	game_map[player.pos_x][player.pos_y-1]='*';
}
void print()//输出在屏幕上
{
	system("cls");//清空控制台
	for (int i=1;i<=map_size;i++)
	{
		for (int j=1;j<=map_size;j++) game_map[i][j]=' ';
	}//地图清空
	for (int i=1;i<N;i++)
	{
		if (bullet[i].vis)
		{
			int xx=bullet[i].pos_x,yy=bullet[i].pos_y;
			for (int j=0;j<4;j++) game_map[xx][yy+j]='|';
		}
	}//子弹覆盖
	for (int i=1;i<N;i++)
	{
		if (plane[i].vis)
		{
			map_cover(i);//覆盖敌机
		}
	}
	check_die();
	player_cover();
	for (int i=1;i<=map_size;i++)
	{
		game_map[i][1]=game_map[i][map_size]=game_map[1][i]=game_map[map_size][i]='#';
	}//输出边框
	cout<<"score:"<<game_score<<"   time:"<<game_time<<"   attack space:"<<(5+max(0,20-attack_average))<<endl;
	//输出分数
	for (int j=1;j<=map_size;j++)
	{
		for (int i=1;i<=map_size;i++)
		{
			cout<<game_map[i][j];
		}
		cout<<endl;
	}//把地图输出到控制台
	if (game_life==0) game_end();
}
void start()//初始化
{
	store=0;//分数初始化
	last_attack=0;//上一次攻击
	game_time=0;//游戏运行帧数
	
	map_size=21;//地图大小，可以修改，但别忘了改最上面的数组大小
	
	player.pos_x=10;//玩家初始化位置
	player.pos_y=20;
	player.size=1;
	
	memset(plane_size,' ',sizeof(plane_size));
	for (int i=1;i<=3;i++) plane_size[1][1][i]='.';
	plane_size[1][2][2]='.';//敌机模型（大小为1）
	
	for (int i=1;i<=5;i++) plane_size[2][1][i]='.';
	for (int i=1;i<=3;i++) plane_size[2][2][i+1]='.';
	for (int i=1;i<=1;i++) plane_size[2][3][i+2]='.';//敌机模型（大小为2）
}
void run_plane()//敌机移动
{
	for (int i=1;i<N;i++)
	{
		if (plane[i].vis)
		{
			plane[i].pos_y++;
			if (plane[i].pos_y>map_size) plane[i].vis=0;//判定出界
		}
	}
}
void create_plane()//随机生成飞机
{
	int cnt=0;
	for (int i=1;i<N;i++)
	{
		if (!plane[i].vis)//判断是否使用
		{
			plane[i].size=rand()%2+1;
			plane[i].pos_y=2;
			plane[i].pos_x=rand()%(map_size-3-plane[i].size)+2;
			//防止有的飞机有一部分在边界
			plane[i].vis=1;
			cnt++;
			if (cnt>=game_time/200+1) return;//达到上限退出
		}
	}
}
void player_move()//玩家移动
{
	int k=check_direction();
	int xx=player.pos_x+dy[k];
	int yy=player.pos_y+dx[k];
	if (k==4) return;
	if (xx>2 && xx<map_size-1 && yy>2 && yy<map_size)//判断是否能移动
	{
		player.pos_x=xx;
		player.pos_y=yy;
	}
}
void player_attack()//玩家攻击
{
	if (KEY_DOWN(VK_SPACE))//检测空格按键
	{
		if (game_time-last_attack>=(5+max(0,20-attack_average)))//计算间隔
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
void run_bullet()//移动子弹
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
void run()//运行函数
{
	while (1)
	{
		game_time++;//game_time是记录游戏帧数
		run_plane();//敌机移动
		if (rand()%(game_time/200+2))
		{
			if (rand()%2) create_plane();
		}
		if (game_time%20==0) game_score++;//每20帧加一分
		player_move();//玩家移动
		player_attack();//玩家攻击
		run_bullet();//子弹移动
		print();//输出到控制台
//		system("pause");
		Sleep(100);
	}
}

