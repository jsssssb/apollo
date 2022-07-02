# from obspy import UTCDateTime, read
# from matplotlib import pyplot as plt
# st_s12 = read('Nakamura2005_deep_moonquake_stacks/A1/S12/combsegy4/Nakamura_2005.A1.combsegy4.S12.MHZ')
# st_s14 = read('Nakamura2005_deep_moonquake_stacks/A1/S14/combsegy4/Nakamura_2005.A1.combsegy4.S14.MHZ')

# print(st_s12, st_s14)
# st_s12.plot(starttime=UTCDateTime('1969-01-01T00:00:00'), endtime=UTCDateTime('1969-01-01T00:08:02'))
# st_s14.plot(starttime=UTCDateTime('1969-01-01T00:00:00'), endtime=UTCDateTime('1969-01-01T00:08:02'))
# plt.show()
#print("hello world")
import calendar
import datetime

def daynum_to_date(year : int, daynum : int) -> datetime.date:
    month = 1
    day = daynum
    while month < 13:
        month_days = calendar.monthrange(year, month)[1]
        if day <= month_days:
            return datetime.date(year, month, day)
        day -= month_days
        month += 1
    raise ValueError('{} does not have {} days'.format(year, daynum))   

print(daynum_to_date(1969, 200))   

 