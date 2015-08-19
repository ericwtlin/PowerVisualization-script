#include<iostream>
#include<fstream>
#include<string>
#include<cstring>
#include<ctime>
/*
�˴�����������population_density_and_charging_station.html�еĳ��վ�������
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
	string BJDistricts[] = { "������","������","��ɽ��","������","��ͷ����","��ƽ��","������",
			"˳����","ƽ����","ͨ����","������","������","��̨��","ʯ��ɽ��","������",
			"������","������","������"};


	//����A����վ
	for(int i = 0; i < 30; i ++){
		
		x = random(116, 117);
		y = random(39.6, 40.2);
		if(restrict(x, y) == false)
			continue;
		
		num ++;
		cout<<BJDistricts[(int)(random(0,17))]<<endl;
		//s1 = Format
		sprintf(info, "{\"item_type\":\"charging_station\",\"name\":\"���վ#%d\",\"type\":\"A��\",\"voltage\":\"220V\",\"power\":\"3000W\",\"location\":\"%s\"},\n",
			num, BJDistricts[(int)(random(0,17))].c_str());
		sprintf(coord, "\"���վ#%d\":{\"x\":%f,\"y\":%f},\n", num, x, y);
		//printf(data);
		ofile_info << info;
		ofile_coord << coord;
		
		
	}

	//����B����վ
	for(int i = 0; i < 30; i ++){
		
		x = random(116, 117);
		y = random(39.6, 40.2);
		if(restrict(x, y) == false)
			continue;
		
		num ++;
		sprintf(info, "{\"item_type\":\"charging_station\",\"name\":\"���վ#%d\",\"type\":\"B��\",\"voltage\":\"220V\",\"power\":\"3000W\",\"location\":\"%s\"},\n",
			num, BJDistricts[(int)(random(0,17))].c_str());
		sprintf(coord, "\"���վ#%d\":{\"x\":%f,\"y\":%f},\n", num, x, y);
		//printf(data);
		ofile_info << info;
		ofile_coord << coord;
		
		
	}

	
	
	ofile_info.close();
	ofile_coord.close();
	return 0;
}
