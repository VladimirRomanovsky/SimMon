#define long32 int
#include "monitoring/monitor.h"
void*        buffer=0;


int date_init(char *file_name)
{
	int status=0;

	char *name = "SimMon1";
	status = monitorDeclareMp(name);
	if ( status!=0 )
    	{
//		printf("ERROR in monitorDeclareMp: %d \n",status);
		return status;
	}
	printf("DataSource: %s \n",file_name) ;
	
	status = monitorSetDataSource(file_name);
	if ( status!=0 )
    	{
//		printf("ERROR in monitorSetDataSource: %d \n",status);
		return status;
	}

	return status;
}

int date_getevent(void* buffer, long size)
{
		int status = monitorGetEvent(buffer,size);
		if ( status!=0 )
		{
//			printf("ERROR in monitorGetEvent: %d \n",status);
		}

		return status;
}
