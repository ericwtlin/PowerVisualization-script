#include<iostream>
#include<fstream>
#include<string>
#include<cstring>
#include<ctime>
/*
此代码用于制作beijing-multigraph.html中的电动车相关数据
*/
using namespace std;

double random(double start, double end)
{
    return start+(end-start)*rand()/(RAND_MAX + 1.0);
}

bool restrict(double x, double y){
	return true;

	
}

int main()
{
	ofstream ofile("electronic_car_info.txt");
	char * info = (char *)malloc(1000);
	char * coord = (char *)malloc(1000);
	int car_num[10];
	srand(unsigned(time(0)));
	int num = 0;
	//18个区县
	string BJDistricts[] = { "密云县","怀柔区","房山区","延庆县","门头沟区","昌平区","大兴区",
			"顺义区","平谷区","通州区","朝阳区","海淀区","丰台区","石景山区","西城区",
			"东城区","宣武区","崇文区"};

	int year_num[] = {2010, 2011, 2012, 2013, 2014};
	
	for(int i = 0; i < 18; i ++){
		for(int j = 0; j < 5; j ++){
			car_num[j] = (int)random(0, 100000);
		}
		
		sprintf(info, "{\"name\":\"%s\",\"bar_data\":{\"x\":[%d, %d, %d, %d, %d], \"y\":[%d, %d, %d, %d, %d]}},\n",
			BJDistricts[i].c_str(),  year_num[0],  year_num[1],year_num[2],year_num[3],year_num[4],car_num[0],car_num[1], car_num[2], car_num[3], car_num[4] );
			
		//printf(data);
		ofile << info;
		
		
	}

	
	ofile.close();
	return 0;
}
