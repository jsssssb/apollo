import csv
from obspy.core.utcdatetime import UTCDateTime


# f = open("levent.1008c", encoding="utf-8")
# print(f.read())
# f.close()

def import_apollo(file):
    
    
    """
        
    Columns     Data
    -------     ---------------------------------------------------------

    2           Year

    3           Day of the year

    4           Signal start time in hours and minutes

    5           Signal stop time in hours and minutes; 9999 if the signal
                continues to the next event
                
    42 - 45     Data quality code (single column for each station):
                1 = no data available for the station
                2 = noisy data
                3 = signal is masked by another, larger event
                4 = compressed plot is clipped (original digital data
                    may not be clipped)
                5 = see comments
                6 = the time recorded with the data is computer-
                    generated, and thus is not exact
                    
    77          Event type:
                A = classified (matching) deep moonquake
                M = unclassified deep moonquake
                C = meteoroid impact
                H = shallow moonquake
                Z = mostly short-period event
                L = LM impact
                S = S-IVB impact
                X = special type77
        
                
    """

    # [year, day, sigstart, sigend, qual_11or12, qual_14, qual_15, qual_16,
    #   en_type] = [[] for _ in range(9)]
    # en_type = []
    # sigstart = []
    # sigend = []
    # year = []
    date_ap = []
    
    with open(file, 'r') as af:
        for line in af:
            (yr, day, sig_start_hour,
            sig_start_min, sig_end_hour, sig_end_min) = (line[2:4], line[5:8], line[9:11],
            line[11:13], line[14:16], line[16:18])
            ev_type = line[76]
            qual_11_or_12, qual_14, qual_15, qual_16 = line[41], line[42], line[43], line[44]
            # f = open("./1.txt", 'a')
            # f.writelines(date_all)
            # f.close()
            # date_yr = date_all[2]
            # date_day = date_all[3]
            # date_start_time = date_all[4]
            # date_stop_time = date_all[5]
            # date_ap.append(date_yr)
            # date_ap.append(date_day)
            # date_ap.append(date_start_time)
            # date_ap.append(date_stop_time)
            # date_ap.append(ev_type)
        
            sig_time = UTCDateTime(year=1900+int(yr), julday=int(day),hour=int(sig_start_hour), minute=int(sig_start_min))
            if sig_end_hour.strip() not in ('99', ''):
                if sig_end_hour < sig_start_hour:
                    # special case when the signal runs on to the next day
                    sig_end_time =  UTCDateTime(year=1900+int(yr),julday=int(day) + 1,hour=int(sig_end_hour), minute=int(sig_end_min))
                else:
                    sig_end_time = UTCDateTime(year=1900+int(yr), julday=int(day),
                    hour=int(sig_end_hour), minute=int(sig_end_min))
                    
            else:
                
                if sig_end_hour.strip() not in (''):
                    sig_end_time = UTCDateTime(year=1900+int(yr), julday=int(day),
                    hour=int(sig_start_hour), minute=int(sig_start_min))
                else:
                    sig_end_time = '0000-00-00T00:00:00.000000Z'
            
            del date_ap[:]
            date_ap.extend([yr, day, sig_start_hour, sig_start_min, sig_end_hour
                            , sig_end_min, qual_11_or_12, qual_14, qual_15, qual_16, ev_type, sig_time, sig_end_time])
            f = open("./original_data.csv", 'a', encoding='utf-8',newline='')
            csv_writer = csv.writer(f)
            csv_writer.writerow(date_ap)
            f.close()
            #print(date_ap)
            # date_all = line.split(' ')
            #使用pandas写入csv文件
            # columns_data = ['year', 'day', 'starthour', 'startmin', 'endhour', 'endmin', '11or12-quality', '14-quality', '15-quality', '16-quality', 'type', 'UTDstime', 'UTDetime']
            # inde = ['i' for i in range(13058)]
            # df = pd.DataFrame(date_ap)
            # # print(len(df))



if __name__ == '__main__':
    file = 'levent.1008c'
    import_apollo(file)
            
