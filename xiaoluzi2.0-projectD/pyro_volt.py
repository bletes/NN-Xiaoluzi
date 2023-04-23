#get Xiaoluzi volt,powers of two zones,logs saved to 'D:\\data\\usb6008'-2023-04-11

import datetime
import numpy as np
from daqmx import NIDAQmxInstrument
from datetime import *
import random
import serial
import time
import autochangeP as auto_change_power
import writeindb as wi
import cnn_my as cn

#save data to logs
def save_data(xpath, y_data):
    name = datetime.now().strftime(f'%Y-%m-%d')
    full_path = xpath+'\\2SPECTRA-'+name+'.txt'
    with open(full_path, 'a') as f:
        time_stamp=(datetime.now() - datetime.strptime('1970-1-1 0:0:0', '%Y-%m-%d %H:%M:%S')).total_seconds()
        wi.wr(data,time_stamp-8*3600)
        f.write('\n'+str(time_stamp) + ' ')
        for xx in y_data:
            f.write(str(xx)+' ')
            
#save other logs
def save_logs(xpath, y_data):
    name = datetime.now().strftime(f'%Y-%m-%d')
    full_path = xpath+'\\logs-'+name+'.txt'
    with open(full_path, 'a') as f:
        time_stamp=(datetime.now() - datetime.strptime('1970-1-1 0:0:0', '%Y-%m-%d %H:%M:%S')).total_seconds()
        f.write('\n'+str(time_stamp) + ' ')
        for xx in y_data:
            f.write(str(xx)+' ')
            
#read data from powersupply
def read_power_data():
    serial_A_zone_powerdata_feedback.write(":MEAS:VOLT?\n".encode('utf-8'))
    volt_powersupplyA_feedback = float(serial_A_zone_powerdata_feedback.readline()[:-1])
    serial_B_zone_powerdata_feedback.write(":MEAS:VOLT?\n".encode('utf-8'))
    volt_powersupplyB_feedback = float(serial_B_zone_powerdata_feedback.readline()[:-1])
    serial_A_zone_powerdata_feedback.write(":MEAS:CURR?\n".encode('utf-8'))
    current_powersupplyA_feedback = float(serial_A_zone_powerdata_feedback.readline()[:-1])
    serial_B_zone_powerdata_feedback.write(":MEAS:CURR?\n".encode('utf-8'))
    current_powersupplyB_feedback = float(serial_B_zone_powerdata_feedback.readline()[:-1])
    return (volt_powersupplyA_feedback * current_powersupplyA_feedback, volt_powersupplyB_feedback * current_powersupplyB_feedback)

#output Sinusoidal_siganl
def sin_wave(A, f, fs, phi, t):
    '''
    :params A:    振幅
    :params f:    信号频率
    :params fs:   采样频率
    :params phi:  相位
    :params t:    时间长度
    '''
    # 若时间序列长度为 t=1s,
    # 采样频率 fs=1000 Hz, 则采样时间间隔 Ts=1/fs=0.001s
    # 对于时间序列采样点个数为 n=t/Ts=1/0.001=1000, 即有1000个点,每个点间隔为 Ts
    Ts = 1/fs
    n = t / Ts
    n = np.arange(n)
    y = A*np.sin(2*np.pi*f*n*Ts + phi*(np.pi/180))
    return y

#updata data every 1s
def update_points(num):
    t2=time.time()
    global time_x_axis, volt_A_zone_y_axis, start_time
    global point_ani
    global time_fix
    global time_start
    global trigger1,time_sequence,ss,ss2,td,tas,tbs,taf,tbf,mode
    t4=time.time()
    if time_sequence[trigger1]<time.time()-time_start<time_sequence[trigger1 + 1]:
        if mode==5:
            if len(td)>=10//4:
                ss,ss2=cn.ou(tas,tbs,td,10)#150c
                #print(ss,ss2)
                ss=float(ss*(tas+taf)/tas)
                ss2=float(ss2*(tbs+tbf)/tbs)
               # print(ss,ss2,(tas+taf),(tbs+tbf))
            else:
                ss=3
                ss2=3
            auto_change_power.ps(ss, ss2, serial_A_zone_powerdata_feedback, serial_B_zone_powerdata_feedback)
        if mode==1 or mode==3:
            auto_change_power.ps(ss[trigger1], ss2[trigger1], serial_A_zone_powerdata_feedback, serial_B_zone_powerdata_feedback)
        trigger1+=1
    t4e=str(time.time()-t4)
    t3=time.time()
    if time_fix!=0:
        try:
            #print('sl',1.000 - ((time.time() - time_fix)%1.0),end='')
            time.sleep(1.000 - ((time.time() - time_fix)%1.0))#set interval 1s
        except:
            print('wrong'+time.ctime())
    t3e=str(time.time()-t3)
    t5=time.time()
    y: object = daq.ai0.capture(
        sample_count=1000, rate=10000,
        max_voltage=5, min_voltage=-5.0,
        mode='single-ended referenced', timeout=3.0)
    y2: object = daq.ai1.capture(
        sample_count=1000, rate=10000,
        max_voltage=5, min_voltage=-5.0,
        mode='single-ended referenced', timeout=3.0)

    t5e=str(time.time()-t5)
    t6=time.time()
    power_A_zone, power_B_zone = read_power_data()
    t6e=str(time.time()-t6)
    t7=time.time()
    global trigger3
    
    trigger3+=1
    data.append(np.mean(y)*100)
    data.append(np.mean(y2)*100)
    data.append(power_A_zone)
    data.append(power_B_zone)
    if time.time()-time_fix>600:
        if ss>0 or tas>data[0]:
            taf+=(tas-np.mean(y)*100)*0.001
        if ss>0 or tas>data[0]:
            tbf+=(tbs-np.mean(y2)*100)*0.001

    if data[0]>500 or data[1]>500:
        auto_change_power.ps(0, 0, serial_A_zone_powerdata_feedback, serial_B_zone_powerdata_feedback)
        mode=2
    if taf>33.0:
        taf=33.0
    if tbf>33.0:
        tbf=33.0
    if taf<-33.0:
        taf=-33.0
    if tbf<-33.0:
        tbf=-33.0
    print(tas+taf,tbs+tbf)
    
    if len(data) >= 1:#data 有1个以后save
        save_data('D:\\data\\usb6008', data)
        tempdata=[np.mean(y)*100,np.mean(y2)*100,power_A_zone,power_B_zone]
        if len(td)>=300:#tem data
            td=td[-299:]+[tempdata]
        else:
            td+=[tempdata]
        #print(td)
        data.clear()

    t7e=str(time.time()-t7)
    save_logs(r"C:\Users\admin\Desktop\xiaoluzi2.0-projectD\logs", ['update_cost_time',str(time.time()-t2),'sleep_time:',t3e,'powerset_time:',t4e,'getT_time:',t5e,'getP_time:',t6e,'savedata_time:',t7e])
    return 0




# tested with NI USB-6001
# which has the following analog inputs:
# first, we allocate the hardware using the automatic hardware
# allocation available to the instrument; this is safe when there
# is only one NIDAQmx instrument, but you may wish to specify a
# serial number or model number for a safer experience
if __name__ == '__main__':
    tas=250
    tbs=250
    mode=5#1recipe2nopower3sin4dll5nn6
    tas=tas-25#normally-20
    taf=0
    tbf=0
    daq = NIDAQmxInstrument(device_name='Dev2')#get Temperature data
    print(daq)
    data = []
    start_time = datetime.now()
    a0=daq.ai0
    a1=daq.ai1
    ##sample_count: the number of samples to take
    ##rate: the frequency at which to sample the input
    ##mode: the mode; valid values: differential, pseudo-differential, /
    ## | singled-ended referenced, singled-ended non-referenced
    y_A_zone_port_feedbackdata = a0.capture(
        sample_count=1000, rate=10000,
        max_voltage=5, min_voltage=-5.0,
        mode='single-ended referenced', timeout=3.0)
    y_B_zone_port_feedbackdata=a1.capture(
        sample_count=1000, rate=10000,
        max_voltage=5, min_voltage=-5.0,
        mode='single-ended referenced', timeout=3.0)
    serial_A_zone_powerdata_feedback = serial.Serial("COM3", baudrate=9600, timeout=1)  # powerdata
    serial_B_zone_powerdata_feedback = serial.Serial("COM4", baudrate=9600, timeout=1)
    time_fix=time.time()
    time_start=time.time()
    trigger1=0
    trigger3=0
    td=[]
    time_sequence=range(0, 60 * 60 * 24 * 3, 60 * 60 * 4)
    #time_sequence=range(0,60*60*24*3,5)
    #time_sequence=range(0,10*6*3,10)
    fs = 0.2
    tlen=1000000
    x = np.arange(0, tlen, 1/fs)
    ss=[30,25,20,15,10,5]
    for i in range(111111):
        ss.append(ss[i])
    ##2023-04-10 matrix
    ss=[]#recipe setup
    #sst=[30,35,20,10,5]#[15,25,40,45]
    sst=[25,40,45,35,15]
    for i in sst:
        for ii in range(len(sst)):
            ss.append(i)
    ss2=[10,30,35,20,5]#[15,25,40,45]
    for i in range((len(ss2)-1)*len(ss2)):
        ss2.append(ss2[i])

            
##    ss2=[30,25,20,15,10,5]
##    for i in range(111111):
##        ss2.append(ss2[i])
##    ss=range(20+10,5,-1)
##    ss2=range(20+10,5,-1)
    #auto_change_power.ps(0, 20, serial_A_zone_powerdata_feedback, serial_B_zone_powerdata_feedback)
    if mode==3:
        time_sequence=range(0,60*60*24*3,5)
        ss=[5,5,5,5,5,5]
        for i in range(111111):
            ss.append(ss[i])
        Sinusoidal_siganl_stack=0
        #for i in list(range(100))[1::2]:
        for i in [x*1 for x in [1,3,5,7,10,13,31,100,301,331,1000,3331,7001,7771,9991,10000]]:
            aa=sin_wave(A=15, f=1/i, fs=fs, phi=0, t=tlen)#+100
            Sinusoidal_siganl_stack+=aa
        ma=Sinusoidal_siganl_stack.max()
        mi=Sinusoidal_siganl_stack.min()
        output_max=40
        output_min=30
        Sinusoidal_siganl_stack= Sinusoidal_siganl_stack / (ma - mi) * (output_max - output_min)
        Sinusoidal_siganl_stack= Sinusoidal_siganl_stack + output_min - Sinusoidal_siganl_stack.min()
        ss2=Sinusoidal_siganl_stack
    if mode==5:
        time_sequence=range(0,60*60*24*3,5)
    print('运行中...')
    
    for i in range(10000000):
        update_points(i)
##    ani = animation.FuncAnimation(fig, update_points, blit=True)#642 set interval
##    plt.legend()
##    plt.show()

