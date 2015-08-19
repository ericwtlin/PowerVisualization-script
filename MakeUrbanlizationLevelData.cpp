#include<iostream>
#include<fstream>
#include<string>
#include<cstring>
#include<ctime>
/*
�˴�����������beijing-multigraph.html�еĳ��л�ˮƽ�������
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
	ofstream ofile("urbanlization_info.txt");
	char * info = (char *)malloc(1000);
	char * coord = (char *)malloc(1000);
	double per_capita_GDP_score, city_population_score, tertiary_industry_score;
	int final_score;
	srand(unsigned(time(0)));
	int num = 0;
	//18������
	string BJDistricts[] = { "������","������","��ɽ��","������","��ͷ����","��ƽ��","������",
			"˳����","ƽ����","ͨ����","������","������","��̨��","ʯ��ɽ��","������",
			"������","������","������"};


	//����A����վ
	for(int i = 0; i < 18; i ++){
		
		per_capita_GDP_score = random(20, 100);
		city_population_score = random(20, 100);
		tertiary_industry_score = random(20, 100);

		final_score = (int)(per_capita_GDP_score*0.3 + city_population_score*0.3 + tertiary_industry_score*0.4);
		
		
		sprintf(info, "{\"name\":\"%s\",\"final_score\":%d, \"detail_data\":[{\"name\":\"�˾�GDP\",\"value\":%f},{\"name\":\"�����˿ڱ���\", \"value\":%f},{\"name\":\"������ҵ����\",\"value\": %f}]},\n",
			BJDistricts[i].c_str(),  final_score,per_capita_GDP_score,city_population_score, tertiary_industry_score );
			
		//printf(data);
		ofile << info;
		
		
	}

	
	ofile.close();
	return 0;
}
