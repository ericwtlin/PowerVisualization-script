#include<iostream>
#include<fstream>
#include<string>
#include<cstring>
#include<ctime>
/*
此代码用于制作beijing-multigraph.html中的城市化水平相关数据
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
	//18个区县
	string BJDistricts[] = { "密云县","怀柔区","房山区","延庆县","门头沟区","昌平区","大兴区",
			"顺义区","平谷区","通州区","朝阳区","海淀区","丰台区","石景山区","西城区",
			"东城区","宣武区","崇文区"};


	//创建A类充电站
	for(int i = 0; i < 18; i ++){
		
		per_capita_GDP_score = random(20, 100);
		city_population_score = random(20, 100);
		tertiary_industry_score = random(20, 100);

		final_score = (int)(per_capita_GDP_score*0.3 + city_population_score*0.3 + tertiary_industry_score*0.4);
		
		
		sprintf(info, "{\"name\":\"%s\",\"final_score\":%d, \"detail_data\":[{\"name\":\"人均GDP\",\"value\":%f},{\"name\":\"城市人口比重\", \"value\":%f},{\"name\":\"第三产业比重\",\"value\": %f}]},\n",
			BJDistricts[i].c_str(),  final_score,per_capita_GDP_score,city_population_score, tertiary_industry_score );
			
		//printf(data);
		ofile << info;
		
		
	}

	
	ofile.close();
	return 0;
}
