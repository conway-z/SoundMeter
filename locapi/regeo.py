#coding=utf-8
import requests
import math
import json
import pandas as pd
def request_data(url):
    req = requests.get(url, timeout=30) # 请求连接
    req_jason = req.json() # 获取数据
    return req_jason

def regeo(url,orgid):
    data = request_data(url)
        # {'status': '1', 'regeocode': {'addressComponent': {'city': '杭州市', 'province': '浙江省', 'adcode': '330114', 'district': '临平区', 'towncode': '330114003000', 'streetNumber': {'number': '583-605号', 'location': '120.303915,30.427531', 'direction': '东', 'distance': '7.08056', 'street': '邱山大街'}, 'country': '中国', 'township': '东湖街道', 'businessAreas': [{'location': '120.310088,30.435432', 'name': '东湖', 'id': '330110'}, {'location': '120.305564,30.402803', 'name': '南苑', 'id': '330110'}], 'building': {'name': [], 'type': []}, 'neighborhood': {'name': '名门天第', 'type': '商务住宅;住宅区;住宅小区'}, 'citycode': '0571'}, 'formatted_address': '浙江省杭州市临平区东湖街道名门天第名门天第园'}, 'info': 'OK', 'infocode': '10000'}
    j = json.dumps(data)
    cont2 = json.loads(j)
    print(cont2)
    addr = cont2['regeocode']['addressComponent']
    province = addr['province']
    city = addr['city']
    adcode = addr['adcode']
    district = addr['district']
    formatted_address = cont2['regeocode']['formatted_address']
    df =pd.DataFrame(columns=('orgid','province','city','adcode','district','formatted_address'))
    df = df.append({'orgid':orgid,'province':province,'city':city,'adcode':adcode,'district':district,'formatted_address':formatted_address},ignore_index=True)
    return df

def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x_pi = 3.14159265358979324 * 3000.0 / 180.0
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]

def geo(url,orgid):
    data = request_data(url)
        # {'status': '1', 'regeocode': {'addressComponent': {'city': '杭州市', 'province': '浙江省', 'adcode': '330114', 'district': '临平区', 'towncode': '330114003000', 'streetNumber': {'number': '583-605号', 'location': '120.303915,30.427531', 'direction': '东', 'distance': '7.08056', 'street': '邱山大街'}, 'country': '中国', 'township': '东湖街道', 'businessAreas': [{'location': '120.310088,30.435432', 'name': '东湖', 'id': '330110'}, {'location': '120.305564,30.402803', 'name': '南苑', 'id': '330110'}], 'building': {'name': [], 'type': []}, 'neighborhood': {'name': '名门天第', 'type': '商务住宅;住宅区;住宅小区'}, 'citycode': '0571'}, 'formatted_address': '浙江省杭州市临平区东湖街道名门天第名门天第园'}, 'info': 'OK', 'infocode': '10000'}
    j = json.dumps(data)
    cont2 = json.loads(j)
    print(cont2)
    addr = cont2['geocodes'][0]
    province = addr['province']
    city = addr['city']
    adcode = addr['adcode']
    district = addr['district']
    location = addr['location']
    formatted_address = addr['formatted_address']
    df =pd.DataFrame(columns=('orgid','province','city','adcode','district','formatted_address','location'))
    df = df.append({'orgid':orgid,'province':province,'city':city,'adcode':adcode,'district':district,'formatted_address':formatted_address,'location':location},ignore_index=True)
    return df

# 按坐标查找，输入坐标类型：高德/百度
def genbylnglat(site):
    file_name = "files/机构.xlsx"
    dfsr = pd.read_excel(file_name, sheet_name='Sheet1')
    dfsr = dfsr[ dfsr['lng'] >100]
    dfout = pd.DataFrame(columns=('orgid','province','city','adcode','district'+site,'formatted_address','location'))
    for row in dfsr.itertuples():
        orgid = getattr(row, 'orgid')
        if site == 'gd':
            # 按高德坐标
            lng = getattr(row, 'lng')
            lat = getattr(row, 'lat')
        else:
            # 按百度坐标，转高德
            lng_bd = getattr(row, 'lng')
            lat_bd = getattr(row, 'lat')
            (lng,lat) = bd09_to_gcj02(lng_bd,lat_bd)
        url = "https://restapi.amap.com/v3/geocode/regeo?location=%s,%s&output=JSON&key=14158a7cefd90570304ff2f0d4efac0e" % (lng, lat)
        try:
            dfout = dfout.append(regeo(url,orgid),ignore_index=True)
        except Exception as e:
            pass
            continue
    dfout = pd.merge(dfsr,dfout,on='orgid',how='left')
    dfout.to_excel('files/dfout-%s.xlsx' % (site))

def genbyaddr():
    file_name = "files/机构.xlsx"
    dfsr = pd.read_excel(file_name, sheet_name='Sheet1')
    dfout = pd.DataFrame(columns=('orgid','province','city','adcode','district','formatted_address'))
    for row in dfsr.itertuples():
        orgid = getattr(row, 'orgid')
        # 按高德坐标
        ct = getattr(row, 'ct')
        addr = getattr(row, 'addr')
        url = "https://restapi.amap.com/v3/geocode/geo?address=浙江省%s%s&output=JSON&key=14158a7cefd90570304ff2f0d4efac0e" % (ct,addr)
        try:
            dfout = dfout.append(geo(url,orgid),ignore_index=True)
        except Exception as e:
            pass
            continue
    dfout = pd.merge(dfsr,dfout,on='orgid',how='left')
    dfout.to_excel('files/dfout-addr.xlsx')

def mergetabs():
    dfsradd = pd.read_excel("files/机构表.xlsx", sheet_name='Sheet1')
    dfsr = pd.read_excel("files/机构.xlsx", sheet_name='Sheet1')
    dfaddr= pd.read_excel("files/dfout-addr.xlsx", sheet_name='Sheet1')
    dfbd =  pd.read_excel("files/dfout-bd.xlsx", sheet_name='Sheet1')
    dfgd=   pd.read_excel("files/dfout-gd.xlsx", sheet_name='Sheet1')
    dfout0 = pd.merge(dfsr, dfsradd[['orgid','dis_base']],on='orgid', how='left')
    dfout1 = pd.merge(dfout0, dfaddr[['orgid','district']],on='orgid', how='left')
    dfout2 = pd.merge(dfout1, dfbd[['orgid','district_bd']], on='orgid', how='left')
    dfout3 = pd.merge(dfout2, dfgd[['orgid','district_gd']], on='orgid', how='left')
    dfout3['dislist'] = dfout3['district'] + ',' + dfout3['district_bd'] + ',' + dfout3['district_gd']
    dfout3['dislist'] = dfout3['dislist'].str.split(',')
    dfout3['dislist'] = dfout3['dislist'].apply(lambda x: "" if type(x) == float else max(x, key=x.count))
    dfout3.to_excel('files/dfout-merge.xlsx')
# genbylnglat('bd')
# genbylnglat('gd')
# genbyaddr()
mergetabs()