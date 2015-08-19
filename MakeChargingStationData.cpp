#include<iostream>
#include<fstream>
#include<string>
#include<cstring>
#include<ctime>
/*
此代码用于制作population_density_and_charging_station.html中的充电站相关数据
*/
using namespace std;

double random(double start, double end)
{
    return start+(end-start)*rand()/(RAND_MAX + 1.0);
}

bool restrict(double x, double y){


	if( x - y <= 77 && x - y >= 76)
		return true;
	else
		return false;
}

int main()
{
	ofstream ofile_info("charging_stations_info.txt");
	ofstream ofile_coord("charging_stations_geoCoord.txt");
	char * info = (char *)malloc(1000);
	char * coord = (char *)malloc(1000);
	double x, y;
	srand(unsigned(time(0)));
	int num = 0;
	string BJDistricts[] = { "密云县","怀柔区","房山区","延庆县","门头沟区","昌平区","大兴区",
			"顺义区","平谷区","通州区","朝阳区","海淀区","丰台区","石景山区","西城区",
			"东城区","宣武区","崇文区"};


	//创建A类充电站
	for(int i = 0; i < 30; i ++){
		
		x = random(116, 117);
		y = random(39.6, 40.2);
		if(restrict(x, y) == false)
			continue;
		
		num ++;
		cout<<BJDistricts[(int)(random(0,17))]<<endl;
		//s1 = Format
		sprintf(info, "{\"item_type\":\"charging_station\",\"name\":\"充电站#%d\",\"type\":\"A类\",\"voltage\":\"220V\",\"power\":\"3000W\",\"location\":\"%s\"},\n",
			num, BJDistricts[(int)(random(0,17))].c_str());
		sprintf(coord, "\"充电站#%d\":{\"x\":%f,\"y\":%f},\n", num, x, y);
		//printf(data);
		ofile_info << info;
		ofile_coord << coord;
		
		
	}

	//创建B类充电站
	for(int i = 0; i < 30; i ++){
		
		x = random(116, 117);
		y = random(39.6, 40.2);
		if(restrict(x, y) == false)
			continue;
		
		num ++;
		sprintf(info, "{\"item_type\":\"charging_station\",\"name\":\"充电站#%d\",\"type\":\"B类\",\"voltage\":\"220V\",\"power\":\"3000W\",\"location\":\"%s\"},\n",
			num, BJDistricts[(int)(random(0,17))].c_str());
		sprintf(coord, "\"充电站#%d\":{\"x\":%f,\"y\":%f},\n", num, x, y);
		//printf(data);
		ofile_info << info;
		ofile_coord << coord;
		
		
	}

	
	
	ofile_info.close();
	ofile_coord.close();
	return 0;
}
