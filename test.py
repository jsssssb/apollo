# from obspy import UTCDateTime, read
# from matplotlib import pyplot as plt
# st_s12 = read('Nakamura2005_deep_moonquake_stacks/A1/S12/combsegy4/Nakamura_2005.A1.combsegy4.S12.MHZ')
# st_s14 = read('Nakamura2005_deep_moonquake_stacks/A1/S14/combsegy4/Nakamura_2005.A1.combsegy4.S14.MHZ')

# print(st_s12, st_s14)
# st_s12.plot(starttime=UTCDateTime('1969-01-01T00:00:00'), endtime=UTCDateTime('1969-01-01T00:08:02'))
# st_s14.plot(starttime=UTCDateTime('1969-01-01T00:00:00'), endtime=UTCDateTime('1969-01-01T00:08:02'))
# plt.show()
#print("hello world")
# import calendar
# import datetime

# def daynum_to_date(year : int, daynum : int) -> datetime.date:
#     month = 1
#     day = daynum
#     while month < 13:
#         month_days = calendar.monthrange(year, month)[1]
#         if day <= month_days:
#             return datetime.date(year, month, day)
#         day -= month_days
#         month += 1
#     raise ValueError('{} does not have {} days'.format(year, daynum))   

# print(daynum_to_date(1969, 200))   
from fileinput import filename
import urllib.request as ur
import os
import sys
# def Schedule(a,b,c):
#     '''''
#     a:已经下载的数据块
#     b:数据块的大小
#     c:远程文件的大小
#     '''
#     per = 100.0 * a * b / c
#     if per > 100 :
#         per = 100
#     print ('%.2f%%' % per)

# def printout(a, b, c):
#     print(str(a) + ", " + str(b) + ", " + str(c))
# local = os.path.join('./1.csv')

# ur.urlretrieve('https://darts.jaxa.jp/planet/seismology/apollo/dump/dump/lp/START_TIME/1971-04-17T07:04:00/STOP_TIME/1971-04-17T09:00:00', local, reporthook=printout)
# filename = 'test_1'
def _progress(block_num, block_size, total_size):
    '''回调函数
        @block_num: 已经下载的数据块
        @block_size: 数据块的大小
        @total_size: 远程文件的大小
    '''
    
    per = (float(block_size) * float(block_num) * 100)  / (float(total_size) * (-4513792))
    if per > 100:
        per = 100
    sys.stdout.write('\r>> Downloading %s %.1f%%' % (filename, per))
    sys.stdout.flush()
# file = open('./1.csv', 'w')
# url_1 =  'https://darts.jaxa.jp/planet/seismology/apollo/dump/dump/lp/START_TIME/1971-04-17T07:04:00/STOP_TIME/1971-04-17T09:00:00'
# local = os.path.join('./1.csv')
# ur.urlretrieve(url_1, local, _progress)
# dir = os.path.join(os.getcwd(), 'download_lunar_data')
i=0
with open('./download_shallowearthquake_data.txt', 'r') as f:
    
    for line in f:
        
        print(line)
        i += 1
        print(i)
        a = "第{}次浅月震记录数据".format(i)
        b = a + '.csv'
        dir = 'download_lunar_data'
        dir_name = os.path.join(dir, b)
        file = open(dir_name, 'w')
        url_ad = line
        ur.urlretrieve(url_ad, dir_name, _progress)
        # for i in range(len(f.readlines())):
        #     if i < 29:

            
                
        # else:
        #     url_ad = line
        #     print(url_ad)

        #ur.urlretrieve(url_ad, dir_name)
        #with open('./download_shallowearthquake_data.txt', 'r') as f:
        
# for i in range(10):
#     print('i================',i)
#     for j in range(10):
#         if j > 5 :
#             continue
#         print(j)
