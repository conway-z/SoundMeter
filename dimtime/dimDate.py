#coding=utf-8
#import utils.lunar as Lunar
from dataqin.dimtime.lunar import Lunar
import pandas as pd
def getLunar(ct=None):
    ln = Lunar(ct)
    return (ln.ln_date_str(), ln.gz_year(), ln.sx_year(), ln.gz_day(),ln.ln_jie())
def holiday(ln_date):
    n = ('春节','春节','春节','端午节','中秋节','元旦','劳动节','国庆节','国庆节','国庆节')
    d = ('腊月三十','正月初一','正月初二','五月初五','八月十五',(1,1),(5,1),(10,1),(10,2),(10,3))
    dic = dict(zip(d,n))
    if ln_date in d:
        return dic[ln_date]
def zodiac(month, day):
    n = ('摩羯座','水瓶座','双鱼座','白羊座','金牛座','双子座','巨蟹座','狮子座','处女座','天秤座','天蝎座','射手座')
    d = ((1,20),(2,19),(3,21),(4,21),(5,21),(6,22),(7,23),(8,23),(9,23),(10,23),(11,23),(12,23))
    return n[len(list(filter(lambda y:y<=(month,day), d)))%12]

def generateData(startDate, endDate):
    d = {'id':pd.date_range(start=startDate, end=endDate)}
    data = pd.DataFrame(d)
    data['year'] = data['id'].apply(lambda x:x.year)
    data['month'] = data['id'].apply(lambda x:x.month)
    data['day'] = data['id'].apply(lambda x:x.day)
    data['quarter'] = data['id'].apply(lambda x:x.quarter)
    data['day_name'] = data['id'].apply(lambda x:x.day_name())
    data['weekof_year'] = data['id'].apply(lambda x:x.weekofyear)
    data['day_of_year'] = data['id'].apply(lambda x:x.dayofyear)
    data['day_sin_month'] = data['id'].apply(lambda x:x.daysinmonth)
    data['day_of_week'] = data['id'].apply(lambda x:x.dayofweek)
    data['is_leap_year'] = data['id'].apply(lambda x:x.is_leap_year)
    data['is_month_end'] = data['id'].apply(lambda x:x.is_month_end)
    data['is_month_start'] = data['id'].apply(lambda x:x.is_month_start)
    data['is_quarter_end'] = data['id'].apply(lambda x:x.is_quarter_end)
    data['is_quarter_start'] = data['id'].apply(lambda x:x.is_quarter_start)
    data['is_year_end'] = data['id'].apply(lambda x:x.is_year_end)
    data['is_year_start'] = data['id'].apply(lambda x:x.is_year_start)
    data['lunar'] = data['id'].apply(lambda x:getLunar(x))
    data['lunar_date'] = data['lunar'].apply(lambda x:x[0])
    data['gz_year'] = data['lunar'].apply(lambda x:x[1])
    data['sx_year'] = data['lunar'].apply(lambda x:x[2])
    data['gz_day'] = data['lunar'].apply(lambda x:x[3])
    data['solar_terms'] = data['lunar'].apply(lambda x:x[4])
    data['zodiac'] = data['id'].apply(lambda x:(x.month,x.day))
    data['holiday0']= data['zodiac'].apply(lambda x:holiday(x))
    data['holiday1']= data['lunar_date'].apply(lambda x:holiday(x))
    data['zodiac'] = data['zodiac'].apply(lambda x:zodiac(x[0],x[1]))
    del data['lunar']
    return data
data =generateData(startDate='1919-1-1', endDate='2049-12-31')
print(data.min)
data.to_csv('DIM_TIME.csv', index = False,index_label = False)
# print(type(data))
