from calendar import day_abbr
from datetime import datetime
from time import time
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from obspy import UTCDateTime, read, Trace, Stream
import decimal
from scipy.fftpack import fft,ifft
from datetime import timedelta
from scipy import signal

# weather = """
# 00.0000 0.0 ??? 4.7 97.7 1015.0 0.0 010308 000000
# 00.0002 0.0 ??? 4.7 97.7 1015.0 0.0 010308 000001
# 00.0005 0.0 ??? 4.7 97.7 1015.0 0.0 010308 000002
# 00.0008 0.0 ??? 4.7 97.7 1015.4 0.0 010308 000003
# 00.0011 0.0 ??? 4.7 97.7 1015.0 0.0 010308 000004
# 00.0013 0.0 ??? 4.7 97.7 1015.0 0.0 010308 000005
# 00.0016 0.0 ??? 4.7 97.7 1015.0 0.0 010308 000006
# 00.0019 0.0 ??? 4.7 97.7 1015.0 0.0 010308 000007
# """

# # Convert to NumPy character array
# data = np.fromstring(weather, dtype='|S1')

# # Fill header attributes
# stats = {'network': 'BW', 'station': 'RJOB', 'location': '',
#         'channel': 'WLZ', 'npts': len(data), 'sampling_rate': 0.1,
#         'mseed': {'dataquality': 'D'}}
# # set current time
# stats['starttime'] = UTCDateTime()
# st = Stream([Trace(data=data, header=stats)])
# # write as ASCII file (encoding=0)
# st.write("weather.mseed", format='MSEED', encoding=0, reclen=256)

# # Show that it worked, convert NumPy character array back to string
# st1 = read("weather.mseed")
# print(st1[0].data.tobytes())
##############################################################################################################################################################################################################################################################################
'''
column 1: frame_count
The raw data are composed of 90 frames, and this is the counter of frames. The frame count cycles through 0 to 89. The detailed description is written in the UTIG Technical Report 118, here: [Tech Report 118.]
原始数据由90帧组成，这是帧计数器。帧计数循环从0到89。详细描述见UTIG技术报告118。

column 2: ap_station
This is apollo station No. (11,12,14,15,16,17)

column 3: ground_station
'ground_station' is the number that corresponds to NASA's Deep Space Network (DSN). You can find out the station name from here: [Data Correction]. Please see the Time Error Correction on the Ground Stations of the URL.
“ground_station”是NASA深空网络(DSN)对应的数字。你可以从这里找到station的名字[Data Correction]。请参阅网址的ground station时间错误更正。

column 4: nc
One frame includes 64 words, and four data for Long Period Seismometer (LP). The following link may be helpful: [Quick Look]
一帧包含64个字，4个长周期地震仪数据。下面的链接可能会有帮助。

column 5: time
The estimated time for the data.
采样的估计时间。

column 6, 7, 8: lpx, lpy, lpz
The digital data of Long Period X, Y, Z. These values are raw data, and are normally used together with the response function, here: [Response]
长周期X、Y、Z的电子数据。这些值为原始数据，通常与响应函数一起使用。
'''
# st = read('./Nakamura_2005.A1.combsegy4.S12.MHZ')
# print(st)
# print(len(st))
# tr = st[0]
# print(tr.stats)
# 读取第一次月震浅震数据体
df = pd.read_csv('./download_lunar_data/第1次浅月震记录数据.csv', engine='python', dtype={'vehicleplatenumber': str, 'device_num': str})
df = pd.DataFrame(df)
# print(os.getcwd())
# print(df.columns)
# print(df.dtypes)
data_12 = df[(df[' ap_station'] == 12)]
# print(data_12)
#data_12.to_csv('./event_1_ap12.csv')
# def seconder(x):
#     mins, secs, millis = map(float, x.split('.'))
#     td = timedelta(minutes=mins, seconds=secs, milliseconds=millis)
#     return td.total_seconds()
# stats['starttime'] = UTCDateTime(data_12_x.iloc[0])
# stats['endtime'] = UTCDateTime(data_12_x.iloc[-1])

# 取前5000个采样点
# 时间
data_12_time = (data_12.iloc[:,4])
data_12_x = data_12_time[0:5000]
stats = UTCDateTime(data_12_time.iloc[0])
state = UTCDateTime(data_12_time.iloc[4999])

stat = state - stats

# 地震数据
data_12_y = data_12.iloc[:,7]
data_12_y = np.array(data_12_y).astype(np.float32)
# dtime = data_12_x.astype('datetime64[ns]')
data_correction = np.where(data_12_y < 800, data_12_y, 511)
data_correction = np.where(data_correction > 0, data_correction, 511)
# 归0
data_correction = data_correction - np.float32(511.0)
# print(len(data_correction))
data_1 = data_correction[0:5000]

# dtime_1 = dtime[0:5000]
# dtime_start = dtime[0].dt.total_seconds()
# dtime_end = dtime[5000].dt.total_seconds()
# dtime_ir = (dtime_end - dtime_start)
# print(dtime_ir)
samples_rate =1.0 / (len(data_1) / stat)


#print(data_12_x)
data_12_x.to_numpy(dtype = 'float32' )

print(samples_rate)
# plt.plot(data_12_x, data_1, 'b')
sos = signal.butter(5, 0.004, 'lp', fs=samples_rate, output='sos')
filtered = signal.sosfilt(sos, data_1)


# plt.plot(data_12_x ,filtered,'r')


plt.show()



# samples = data_12_y.size
# time1  = UTCDateTime("1969-01-01T00:00:00.000000Z")
# time2 = UTCDateTime("1969-01-01T00:08:02.857066Z")
# time3 = time2 - time1
# decimal.getcontext().prec = 15
# d1 = decimal.Decimal(3200.0) / decimal.Decimal(time3)
# (d2) = decimal.Decimal(1.0) / decimal.Decimal(d1)
# print(d2)
# t_s = UTCDateTime(data_12_x.iloc[0])
# t_e = UTCDateTime(data_12_x.iloc[-1])
# print(t_s, t_e)
# t = t_e - t_s

# print(type(t))
# sampling_rate = (t_e - t_s) / samples
# t_d = 1.0 / sampling_rate
# print(type(t_d))
# t_u = t_s * t_d
# print(t_u)
# print(data_12_y)
# print(data_12_y.dtype)
# 暂时注释，调试程序！！！！
# # Fill header attributes
# stats = {'network': 'XA', 'station': 'S12', 'location': '', 'sampling_rate': 1/sampling_rate, 'delta': sampling_rate, 
#         'channel': 'MHZ', 'npts': len(data_12_y),
#         'mseed': {'dataquality': 'D'}}
# # for i in data_12_x.index:
    
# #     t_i = UTCDateTime(data_12_x[i])
    
# # set current time
# stats['starttime'] = UTCDateTime(data_12_x.iloc[0])
# stats['endtime'] = UTCDateTime(data_12_x.iloc[-1])
# #print(stats['endtime'])
# st = Stream([Trace(data=data_12_y, header=stats)])
# # write as ASCII file (encoding=0)
# st.write("try_1.MHZ", format='MSEED', encoding=4, reclen=65536)
# # ########################################################################
# st1 = read('./try_1.MHZ')
# tr = st1[0]
# print(st1)
# # !!!!!修改、测试代码是否正确-工作区!!!!!!!!!!
# tt = data_12_x[:0]
# print(tt)
# print(data_12_x.index)
# 
# print(data_12_x.dtypes)
# data_12_x0 = int(data_12_x[0].timestamp())

# t_1 = UTCDateTime(data_12_x.iloc[-1])

# print(t_1)
#########################################################################




