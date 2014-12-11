//Read the raw data from the GPS and convert it ti time, altitude and longitude
//this program takes two values, time (in seconds) and name of file.
//default values, time = 60 and file = gps_recording
#include <iostream>
#include <unistd.h>
#include <signal.h>
#include <time.h>
#include <cstring>
#include <cstdio>


using namespace std;
typedef struct 
{
	char fileName[30];
	int timeS; //time in seconds
	FILE* dataFile;
} Parameters;

//Just read the parameters given to the function 
void read_arguments(int argc, char* argv[], Parameters* param) {
	
	if (argc == 2) { // just the name of the file to read is given
		printf("File: ");
		scanf("%s", param->fileName);
		//strcpy(param->fileName, "gps_recording_ceramic.txt");
		param->timeS = 60;
		param->dataFile = fopen(argv[1], "r"); 
		if (param->dataFile == NULL){
			cerr << "Can't open file" << endl;
			exit(-1);
		}
	} else {
		strcpy(param->fileName, argv[1]);
		param->timeS = atoi(argv[2]);
		param->dataFile = fopen(argv[3], "r");
		if (param->dataFile == NULL){
			cerr << "Can't open file" << endl;
			exit(-1);
		}
	}
}

//Time Format Change the format of the time into human readable values
//char* read_time(char* time) {

//}

//Change latitude and longitude into decimal

//parse message GPGGA and create a new file
void parse_data(FILE* newFile, char* data) {

	char buffer[20];
	char* token;
	int spaceMsg = 0;

	token = strtok(data, ",");

	while((token != NULL) && (spaceMsg <= 5)) {
		switch (spaceMsg) {
			case 0:
				fprintf(newFile, "Format: %s\n", token);
				break;
			case 1:
				fprintf(newFile, "Time: %s\n", token);
				break;
			case 2:
				fprintf(newFile, "Latitude: %s ", token);
				break;
			case 3:
				fprintf(newFile, "Direction: %s\n", token);
				break;
			case 4:
				fprintf(newFile, "Longitude: %s ", token);
				break;
			case 5:
				fprintf(newFile, "Direction: %s\n", token);
				break;
			default:
				cerr << "Error parsing message" << endl;
				exit(-1);
		}
		spaceMsg++;
		token = strtok(NULL, ",");
	}

	fprintf(newFile, "\n");
}

//Read the files and create a new file 

void read_data(char* fileName, FILE* dataFile) {

	char buffer[83], buffer2[83];
	char msgFormat[] = "GPGGA"; 
	FILE* newFile = fopen(fileName, "w+");

	if (newFile == NULL) {
		cerr << "Can't create new file" << endl;
		exit(-1);
	}

	memset(buffer, 0, 83); //clear buffer
	memset(buffer2, 0, 83); //clear buffer

	while(fgets(buffer, 83, dataFile) != NULL) {
		buffer[strlen(buffer) - 1] = 0; //get rid off newline
		strcpy(buffer2, buffer + 1); //get rid off '$'
		if (strncmp(buffer2, msgFormat, 5) == 0) {
			parse_data(newFile, buffer2);
		}
		memset(buffer, 0, 83);
		memset(buffer2, 0, 83);
	}

	fclose(newFile);
}


int main (int argc, char* argv[])
{
	Parameters param;
	//pid_t pid

	read_arguments(argc, argv, &param);
	read_data(param.fileName, param.dataFile);
	//pid = fork();


	//if (!pid) { //Child process

	//}


	//cout << param.fileName;
	//cout << " time: " << param.timeS << endl;
	fclose(param.dataFile);
	return 0;
}