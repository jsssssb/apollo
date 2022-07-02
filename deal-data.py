#!D:\miniconda3\envs\tf-base tf-base python=3.8
#coding:utf-8
import pandas as pd



csv_data = pd.read_csv('./2.csv')
csv_data.columns = ['year', 'day', 'starthour', 'startmin', 'endhour', 'endmin','11or12-quality', '14-quality','15-quality', '16-quality', 'type', '标准开始时间', '标准结束时间']
df = pd.DataFrame(csv_data)

# 把day列从str 转化为 int64
# df['day'] = df['day'].astype('int64')
# df['year'] = df['year'].astype('int64')


# def daynum_to_date(year_in : int, daynum : int) -> datetime.date:
#     month = 1
#     day = daynum
#     while month < 13:
#         month_days = calendar.monthrange(year_in, month)[1]
#         if day <= month_days:
#             return datetime.date(year_in, month, day)
#         day -= month_days
#         month += 1
#     raise ValueError('{} does not have {} days'.format(year_in, daynum))

#print(df)
# for column in df[['year']]:
#         columnSeriesObj = df[column] 
#         print('Colunm Name : ', column) 
#         print('Column Contents : ', columnSeriesObj.values)
#         year_real = 1900 + columnSeriesObj
#         df.iloc[:,0] = year_real
#         for column in df[['day']]:
#             columnSeriesObj = df[column]
#             daynum = columnSeriesObj
#             year_in = year_real
data_shallow = df[(df['type']== 'H')]

data_deep=df[df['type'].isin(['A', 'M'])]
# data_shallow.to_csv('./shallow_q.csv',index =True ,sep = ',')
# df.to_csv('./data_all.csv', index = True, sep = ",")
#print(data_deep)
print(data_shallow.index)






