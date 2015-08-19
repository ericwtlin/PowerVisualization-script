#include<iostream>
#include<fstream>
#include<string>
#include<ctime>
/*
�˴�����������population_density_and_charging_station.html�е�heat_data
*/
using namespace std;

double random(double start, double end)
{
    return start+(end-start)*rand()/(RAND_MAX + 1.0);
}

bool restrict(double x, double y){


	if( x - y <= 77 && x - y >= 75)
		return true;
	else
		return false;
}

int main()
{
	string filename = "heatdata.txt";
	ofstream ofile(filename);
	char * data = (char *)malloc(1000);
	double x, y;
	double value;
	int repeat_num;
	srand(unsigned(time(0)));

	//���������귶Χ:��γ39��26����41��03��������115��25���� 117��30��
	for(int i = 0; i < 30; i ++){
		
		x = random(116.3, 116.5);
		y = random(40.4, 40.5);
		if(restrict(x, y) == false)
			continue;
		value = random(0, 300);
		repeat_num = (int)random(1, 5);
		for( int j = 0; j < repeat_num; j ++){
			sprintf(data, "[%f, %f, %f],\n", x, y, value);
			//printf(data);
			//printf("%d", sizeof(data));
			ofile << data;
		}
		
	}

	for(int i = 0; i < 30; i ++){
		
		x = random(115.8, 116);
		y = random(39.7, 39.8);
		if(restrict(x, y) == false)
			continue;
		value = random(0, 500);
		repeat_num = (int)random(1, 5);
		for( int j = 0; j < repeat_num; j ++){
			sprintf(data, "[%f, %f, %f],\n", x, y, value);
			//printf(data);
			//printf("%d", sizeof(data));
			ofile << data;
		}
		
	}
	int data_length = 100;
	for(int i = 0; i < data_length ; i ++){
		
		x = random(115.4, 117.5);
		y = random(39.5, 41.0);
		if(restrict(x, y) == false)
			continue;
		value = random(0, 100);
		repeat_num = (int)random(1, 20);
		for( int j = 0; j < repeat_num; j ++){
			sprintf(data, "[%f, %f, %f],\n", x, y, value);
			//printf(data);
			//printf("%d", sizeof(data));
			ofile << data;
		}
		/*
		for( int j = 0; j < repeat_num; j ++){
			if(i != data_length - 1 || j != repeat_num - 1){
				sprintf(data, "{\"x\":%f,\"y\":%f,\"value\":%f},\n", x, y, value);
				//printf(data);
				//printf("%d", sizeof(data));
				ofile << data;
			}else{
				sprintf(data, "{\"x\":%f,\"y\":%f,\"value\":%f}\n", x, y, value);
				//printf(data);
				ofile << data;
			}
		}
		*/
	}
	
	ofile.close();
	return 0;
}
