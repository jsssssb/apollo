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
            del date_ap[:]
            
            # date_all = line.split(' ')
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
                if sig_end_hour.strip() in ('99'):
                    sig_end_time = UTCDateTime(year=1900+int(yr), julday=int(day),
                    hour=int(sig_start_hour), minute=int(sig_start_min))
                    

            date_ap.extend([yr, day, sig_start_hour, sig_start_min, sig_end_hour
                            , sig_end_min, qual_11_or_12, qual_14, qual_15, qual_16, ev_type, sig_time, sig_end_time])
            f = open("./2.csv", 'a', encoding='utf-8',newline='')
            # f.writelines(date_ap)
            csv_writer = csv.writer(f)
            csv_writer.writerow(date_ap)
            f.close()
            
            # f = open("./t-1.csv", 'a', encoding='utf-8', newline='')
            # csv_writer = csv.writer(f)

            # csv_writer.writerow(date_ap)
            
            # f.close()

            #print(date_ap)
            # yr = line[2:4]
            # print(yr)
            # date_ap.append(list(line[5:8].strip().split(',')))

            # 2. 创建文件对象
            # f = open("./test.csv",'w',encoding='utf-8',newline='')
            # writer = csv.writer(f)
            # writer.writerows(date_ap)
            # f.close() 
            # f = open("./test.csv",'a',encoding='utf-8',newline='')

            # csv_writer = csv.writer(f)

            # csv_writer.writerow(date_ap)
            
            # f.close()
            

            # sig_time = UTCDateTime(year=1900+int(date_yr), julday=int(date_day),hour=int(sig_start_hour), minute=int(sig_start_min))
            # if sig_end_hour.strip() not in ('99', ''):
            #     if sig_end_hour < sig_start_hour:
            #         # special case when the signal runs on to the next day
            #         sig_end_time = sig_end_time = UTCDateTime(year=1900+int(yr),julday=int(day) + 1,hour=int(sig_end_hour), minute=int(sig_end_min))
            #     else:
            #         sig_end_time = UTCDateTime(year=1900+int(yr), julday=int(day),hour=int(sig_end_hour), minute=int(sig_end_min))
            
            # datetime.append(sig_time)
            # f = open("./t-1.csv", 'a', encoding='utf-8', newline='')
            # csv_writer = csv.writer(f)

            # csv_writer.writerow(datetime)
            
            # f.close()

            
            #print(type(sig_time))
            #print(type(sig_end_time))


if __name__ == '__main__':
    file = 'levent.1008c'
    import_apollo(file)
            
            









    

            
            
            # read the original file
            # (yr, day_ori, sig_start_hour_ori,
            #  sig_start_min_ori, sig_end_hour_ori, sig_end_min_ori,
            #  env_11_or_12, env_14, env_15, env_16, av_11_or_12, av_14, av_15,
            #  av_16, qual_11_or_12_ori, qual_14_ori, qual_15_ori, qual_16_ori, comments, ev_type_ori,
            #  matching_moonquake, moonquake_type, moonquake_number
            #  ) = (line[2:4], line[5:8], line[9:11],
            #       line[11:13], line[14:16], line[16:18],
            #       line[19:22], line[23:26], line[27:30], line[31:34], line[36],
            #       line[37], line[38], line[39],
            #       line[41], line[42], line[43],
            #       line[44], line[46:76], line[76], line[77:80], line[81], line[82:85])
            # day = []
            # day.append((day_ori).strip().split(',')[0])
            
            
            
            
            #print(day)
#             date_time = daynum_to_date(year, day)
#             with open("test.csv", "w") as csvfile:
#                 writer = csv.writer(csvfile)
                
#                 writer.writerow(["年", "日期"])
#                 writer.writerow([[year], [date_time]])
                

            # sig_start_time = UTCDateTime(year=1900+int(yr), julday=int(day_ori),
            # hour=int(sig_start_hour_ori), minute=int(sig_start_min_ori))
            
            # print(UTCDateTime(sig_start_time))
            # sig = str(sig_start_time)
            # print(sig)
            # note = open('./data.txt', mode = 'w')
            # note.write(sig)
            
            
            
            # if sig_end_hour_ori.strip() not in ('99', ''):
            #     if sig_end_hour_ori < sig_start_hour_ori:
            #         # special case when the signal runs on to the next day
            #         sig_end_time = UTCDateTime(year=1900+int(yr), julday=int(day_ori) + 1,
            #           hour=int(sig_end_hour_ori), minute=int(sig_end_min_ori))
            #     else:
            #         sig_end_time = UTCDateTime(year=1900+int(yr), julday=int(day_ori),
            #           hour=int(sig_end_hour_ori), minute=int(sig_end_min_ori))
                    
            # sigstart.append(sig_start_time)
            # sigend.append(sig_end_time)
            # ev_type_tf = ''.join(ev_type_ori)
            # en_type.append(ev_type_tf)
                    
            

    #         year_tf = ''.join(yr)
    #         day_tf = ''.join(day_ori)
    #         sig_start_hour_tf = ''.join(sig_start_hour_ori)
    #         sig_start_min_tf = ''.join(sig_start_min_ori)
    #         sig_end_hour_tf = ''.join(sig_end_hour_ori)
    #         sig_end_min_tf = ''.join(sig_end_min_ori)
    #         qual_11or12_tf = ''.join(qual_11_or_12_ori)
    #         qual_14_tf = ''.join(qual_14_ori)
    #         qual_15_tf = ''.join(qual_15_ori)
    #         qual_16_tf = ''.join(qual_16_ori)
    #         sig_start = sig_start_hour_tf + sig_start_min_tf
    #         sig_end = sig_end_hour_tf + sig_end_min_tf

    #         year.append(year_tf)
    #         day.append(day_tf)
    #         sigstart.append(sig_start)
    #         sigend.append(sig_end)
    #         qual_11or12.append(qual_11or12_tf)
    #         qual_14.append(qual_14_tf)
    #         qual_15.append(qual_15_tf)
    #         qual_16.append(qual_16_tf)


    
    
    #df = pd.DataFrame({'year': year, 'day': day, 'sig_start': sig_start, 'sigend': sigend, 
    #                    'qual_11or12':  qual_11or12, 'qual_14': qual_14, 'qual_15': qual_15, 
    #                    'qual_16': qual_16, 'en_type': en_type
    #                    })
    # 
        # df = pd.DataFrame({'开始时间': sig_start_time, '结束时间': sig_end_time, '月震类型': en_type})
        # df.to_csv("./data.csv", index = False)

# df = pd.read_csv('test.csv', header=None, names=["day"])
# df.to_csv("./data.csv", index = False)

