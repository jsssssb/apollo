#!D:\miniconda3\envs\base-k base-k python=3.8
#coding:utf-8

import pandas as pd
from fileinput import filename
import urllib.request as ur
import os
import sys
pd.set_option("display.max_colwidth",1000)
pd.set_option('display.max_rows', 100) # 显示的最大行数（避免只显示部分行数据）
pd.set_option('display.max_columns', 1000) # 显示的最大列数（避免列显示不全）
pd.set_option("display.max_colwidth",1000) # 每一列最大的宽度（避免属性值或列名显示不全）
pd.set_option('display.width',1000) # 每一行的宽度（避免换行）)
original_data_path = './original_data.csv'
csv_data = pd.read_csv(original_data_path)
csv_data.columns = ['year', 'day', 'starthour', 'startmin', 'endhour', 'endmin',
'11or12-quality', '14-quality',
'15-quality', '16-quality', 
'type', 'UTDstime', 'UTDetime']
df = pd.DataFrame(csv_data)
data_shallow = df[(df['type'] == 'H')]
data_deep=df[df['type'].isin(['A', 'M'])]
print(data_shallow.dtypes)

# 关于去掉月震事件时间数据格式不规范的操作范例，及如何处理一列object数据，使其去掉一部分特定的值
#    City    Date
#0   福州  2021年03月01日
#1   厦门  2021年03月02日
#2   深圳  2021年03月03日
#3   武汉  2021年03月04日
#4   上海  2021年03月05日
#5   青岛  2021年03月06日
#6   烟台  2021年03月07日
#7   荆州  2021年03月08日
#方法一
#pattern = "|".join(["年","月","日"])
#demo.Date = demo.Date.str.replace(pattern, "-")
#demo.Date.str.rstrip("-")

#方法二
#demo.Date.str.strip().replace(dict(zip(["年","月","日"],["-","-",""])), regex=True)

#方法三
# temp = demo.Date.str.extract('(\d+).*?(\d+).*?(\d+)') 
# temp
# temp[0]+"-"+temp[1]+"-"+temp[2]

# 默认纵向拼接，横向拼接默认索引全保留

shallow_st = data_shallow.UTDstime.str.strip().replace(dict(zip([".000000Z"], [""])), regex = True)
shallow_en = data_shallow.UTDetime.str.strip().replace(dict(zip([".000000Z"], [""])), regex = True)

shallow_time = pd.concat([shallow_st, shallow_en], axis = 1, join = 'outer')
#print(shallow_time)

# 删除原数据最后两列，并将整理好格式的数据添加到原数据中

data_shallow = data_shallow.drop(['UTDstime', 'UTDetime'], axis = 1)
data_shallow = pd.concat([data_shallow, shallow_time], axis = 1, join = 'outer')
#print(data_shallow)
# 把 endhour 和 endmin 列从str 转化为 int64
# 不对
# df['endhour'] = df['endhour'].astype('float')
# df['endmin'] = df['endmin'].astype('float')

# 生成浅震地震数据下载链接
f = open('./download_shallowearthquake_data.txt', 'a', encoding= 'utf-8')
for row in data_shallow.itertuples():
    f_write = 'https://darts.jaxa.jp/planet/seismology/apollo/dump/dump/lp/START_TIME/' + getattr(row, 'UTDstime') + '/STOP_TIME/' + getattr(row, 'UTDetime')
    f.write(f_write)
    f.write('\r')
f.close()


# all_url_file_path='./download_shallowearthquake_data.txt'
# download_hdf_file_path='./download_lunar_data'
# lost_url_file_path='./error_url.txt'

# download_hdf=os.listdir(download_hdf_file_path)

# with open(all_url_file_path,'r') as all_url_file:
#     all_url=all_url_file.readlines()
#     for url in all_url:
#         url_single_hdf=urllib.request.urlretrieve(url)
#         if url_single_hdf not in download_hdf:
#             with open(lost_url_file_path,'a') as lost_url_file:
#                 lost_url_file.write(url)
    # print('https://darts.jaxa.jp/planet/seismology/apollo/dump/dump/lp/START_TIME/' + getattr(row, 'UTDstime') + '/STOP_TIME/' + getattr(row, 'UTDetime'))

#data_shallow.to_csv('shallow_earthquake_catalog.csv', encoding= 'utf-8', index= True)

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

with open('./download_shallowearthquake_data.txt', 'r') as f:
    
    for i in range(len(f.readlines())):
        a = "第{}次浅月震记录数据".format(i+1)
        b = a + '.csv'
        dir = 'download_lunar_data'
        dir_name = os.path.join(dir, b)
        file = open(dir_name, 'w')
        with open('./download_shallowearthquake_data.txt', 'r') as f:
            for line in f:
                url_ad = line
                ur.urlretrieve(url_ad, dir_name, _progress)
                break
            




