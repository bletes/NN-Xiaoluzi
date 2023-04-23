#read and write new data into influxdatabase

import pandas as pd 
#import re
#import time
import os
#import matplotlib.pyplot as plt
#import sys

file_dir=r"D:\data\usb6008"
all_file_list=os.listdir(file_dir)
for single_file in all_file_list:
    # 逐个读取
    if single_file[:8]=='2SPECTRA':
        single_data_frame=pd.read_csv(
                os.path.join(file_dir,single_file),sep=' ',index_col=False,names = [0,'T1','T2','P1','P2'],on_bad_lines='skip')
        if single_file ==all_file_list[0]:
                all_data_frame=single_data_frame
        else:  #进行concat操作       
             all_data_frame=pd.concat([all_data_frame,
                    single_data_frame],ignore_index=True)
f2=all_data_frame
f2.index=pd.to_datetime(f2.loc[:,0],unit='s')
f2=f2.loc[:,'T1':]
pd1=pd.DataFrame()
pd1.index=f2.index
pd1['_niv_temperature_A']=f2['T1']
pd1['_niv_temperature_B']=f2['T2']
pd1['_power_A']=f2['P1']
pd1['_power_B']=f2['P2']
#from datetime import datetime
from influxdb_client import InfluxDBClient,Point,WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
token = "OTRy4eHIzV18SgyxJhKJZDXquXP-0NXvSO3UNTTt2UJxu7D63ItNBa3yYXYxP_cPVNmdX_HHSqIDF6vOwRteSw=="
org = "CYTEK"
bucket = "Xiaoluzi"
client = InfluxDBClient(url="http://localhost:8086", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)
write_api.write(bucket, org, record=pd1, data_frame_measurement_name='measurement',
                    data_frame_tag_columns=['measurement'])#{}.format("'2022-12-11 15:00:00'"))
client.close()
print('success')
