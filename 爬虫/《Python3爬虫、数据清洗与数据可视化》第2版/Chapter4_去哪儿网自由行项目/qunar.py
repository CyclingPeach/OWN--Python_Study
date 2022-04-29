import urllib.request
import time
import requests
import pymongo

client = pymongo.MongoClient('localhost', 27017)
book_qunar = client['qunar']
sheet_qunar_zyx = book_qunar['qunar_zyx']


"""
    获取目的地产品列表
"""
def get_list(dep, item):
# for item in a:  # a是目的地列表。现在的a是出发地在澳门，目的地的列表
    url = 'https://touch.dujia.qunar.com/list?modules=list%2CbookingInfo%2CactivityDetail&dep={}&query={}&dappDealTrace=true&mobFunction=%E6%89%A9%E5%B1%95%E8%87%AA%E7%94%B1%E8%A1%8C&cfrom=zyx&it=dujia_hy_destination&date=&needNoResult=true&originalquery={}&width=480&height=320&quality=90&limit=0,20&includeAD=true&qsact=search'.format(
        urllib.request.quote(dep), 
        urllib.request.quote(item + '自由行'), 
        urllib.request.quote(item + '自由行')
    )
    time.sleep(1)
    strhtml = requests.get(url)
    try:
        routeCount = int(strhtml.json()['data']['limit']['routeCount'])
    except:
        return
    # 分20组获取routeCount个产品并存储
    for limit in range(0, routeCount, 20):
        url = 'https://touch.dujia.qunar.com/list?modules=list%2CbookingInfo%2CactivityDetail&dep={}&query={}&dappDealTrace=true&mobFunction=%E6%89%A9%E5%B1%95%E8%87%AA%E7%94%B1%E8%A1%8C&cfrom=zyx&it=dujia_hy_destination&date=&needNoResult=true&originalquery={}&width=480&height=320&quality=90&limit={},20&includeAD=true&qsact=search'.format(
            urllib.request.quote(dep), 
            urllib.request.quote(item + '自由行'), 
            urllib.request.quote(item + '自由行'),
            limit
        )
        strhtml = requests.get(url).json()
        result = {
            'date':time.strftime('%Y-%m-%d', time.localtime(time.time())),   # 重要——需要掌握
            'dep':dep,
            'arrive':item,
            'limit':limit,
            'result':strhtml
        }
        sheet_qunar_zyx.insert_one(result)


def connect_mongo():
    client = pymongo.MongoClient('localhost', 27017)
    book_qunar = client['qunar']
    return book_qunar['qunar_zyx']


"""
    获取网页中json格式数据
"""
def get_json(url):
    strhtml = requests.get(url)
    time.sleep(1)
    return strhtml.json()



def get_all_data(dep):
    a = []
    # 每个 出发地dep 对应的 目的地url
    url = 'https://touch.dujia.qunar.com/golfz/domestic/domesticDest?dep={}&exclude=&extensionImg=255,175'.format(urllib.request.quote(dep))
    # urllib.request.quote(dep)     将中文编码成带%的
    time.sleep(1)
    arrive_dict = get_json(url)     # 目的地列表源代码数据（json格式）
    for arr_item in arrive_dict['data']['ossData']:
        for arr_item_1 in arr_item['subModules'][1:]:
            for query in arr_item_1['items']:
                if query['query'] not in a:
                    a.append(query['query'])    # “query['query']”：目的地的地名
    """
        获取 【出发地dep >>> 所有的目的地a[] >>> 的所有产品】
        在这个for循环下 指的是: “1 个出发地dep” 的 “所有目的地a[]” 的 “所有产品”
        所有数据都存储在“sheet_qunar_zyx”表下面
    """
    for item in a:
        get_list(dep, item)



"""
    出发地>>>398个城市列表——统计时间2022.4.24
"""
dep_list = []
url = 'https://touch.dujia.qunar.com/depCities.qunar'
dep_dict = get_json(url)
for dep_item in dep_dict['data']:
    for dep in dep_dict['data'][dep_item]:
        dep_list.append(dep)