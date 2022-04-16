import time
import pandas
import requests
import random

#获取json数据 ul:10条json数据链接，hd:封装请求头
def get_tap(ul,hd):
    js_list=[]
    #一次性获取所有json数据，并存入js_list
    for url in ul:
        time.sleep(random.randint(1,5))
        json_data=requests.get(url, headers=hd).json()
        js_list.append(json_data)
    jsdata(js_list)

#解析json数据获取数据
def jsdata(js):
    taplist=[]
    for b in js:#遍历10个json数据表
        for i in range(10):#每条json数据有10个评论
            tapdict = {}
            #数据是json嵌套存储，reviews的值
            js_data=b['data']["list"][i]['moment']['extended_entities']['reviews'][0]
            tapdict["用户id"]=js_data['author']['id']
            tapdict["用户名"] = js_data['author']['name']
            tapdict["评论id"]=js_data["id"]
            tapdict['分数']=js_data['score']
            tapdict["评论id"] = js_data["id"]
            #设备和游戏时长有的没有数据
            if js_data['device']=="":
                tapdict["设备"] = "未知"
            else:
                tapdict["设备"]=js_data['device']
            if js_data["played_tips"]=="":
                tapdict["游戏时长"]="未知"
            else:
                tapdict["游戏时长"] = js_data["played_tips"]
            #时间戳转换
            tapdict['评论创建时间'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(float(js_data['created_time'])))
            tapdict['评论更新时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(js_data['updated_time'])))
            tapdict["评论内容"] = js_data['contents']["text"]
            tapdict["点赞量"] = js_data['ups']
            #将数据的字典存入列表
            taplist.append(tapdict)
    save(taplist)

def save(taplist):
    #使用pandas存入Excel
    df=pandas.DataFrame(taplist)
    df.to_excel("taptap评论1.xlsx")

if __name__=="__main__":
    #封装请求头，TapTap网站获取数据会验证cookie信息，所以要封装完整的请求头
    headers = {
            'cookie': 'locale=zh_CN; _uab_collina=164941289783757319708019; tap_theme=light; _gid=GA1.2.63697916.1649851986; acw_tc=276077e116498540208453819e42b48a5888922580bc6b0fc4157174abd7db; _gat=1; _ga_6G9NWP07QM=GS1.1.1649854020.9.1.1649854022.0; _ga=GA1.1.1387153200.1649412898; XSRF-TOKEN=eyJpdiI6IkxCSitmd2lMNzFZUE81U2hqRk9Lb2c9PSIsInZhbHVlIjoiVG05aVBjVnZ1RU5ET2ZEQ1lmNk1EWlNWaldVUHhJUXNxM28zemVmNW5NWjBEYzgwam1RSGptaEVmNE1yR0lXZllIeDV3a0xBbWEzV3pHa25uVkdCZ1E9PSIsIm1hYyI6ImY5MmEwMTM3YTA4MzYwZmZjYjM5YmMxOTZlMGJmMzMxYTg2ZDdhOTliMGMxZDBjMTVkZjRjNDA4Njk1MDBhN2IifQ%3D%3D; tap_sess=eyJpdiI6IklRMVJtZ1JwZjMrRHo4TDJFUzUyY3c9PSIsInZhbHVlIjoiemFXYUpua0VrenBCTVV3QWZpb0Y3U2F2ZkQ0RmZDYkdcL1hQWXViYTMycXloODVqVCtwYU1lR3RBZWNsWGhtU1dhQkM0NGl6bWprdkVsQWE4dUUwNzZ3PT0iLCJtYWMiOiJmYzkyMGNhZTg4ZDc5YjA5ZmQ1MzViYTJiMTdhMGI1NGJkZGJjMzI2MmIxOTdhYzhkYzVhZDA1NTYyZDQxN2Q5In0%3D; ssxmod_itna=Qqmx0DyDBDcD2ACGCDzxA2r1DkjRIp2he+pK4wKDstEDSxGKidDqxBepjp+xcxxqq3iA3BDsK92fPxaYm7Gpx5rLSw4GLDmKDy3Ch4GGjxBYDQxAYDGDDPDo2PD1D3qDkD7r=CScOqi3Dbr=Di4D+WwQDmqG0DDt7n4G2D7tc7BDc3WLevdRBKAi5Ci=DjkbD/+hT=i6KraaqRLiiPPiaYqGy0PGufktZB3bDCE6ZjqisjiP4QE54WG+xF9xeegqzGKq53DhtQ0g5j9h1iiq3Soq5DD3fRD1xD==; ssxmod_itna2=Qqmx0DyDBDcD2ACGCDzxA2r1DkjRIp2he+pK4qikEtKqkDlr7EDj4x2=qx4jaZG83G6EKw8tKie7=o0iWMHjGxMx6AcAcSOMHdOyD4M7idwqLQvh82RpulXCErKPFi5cq/KQzpyLwyzfoIkDbvOLhvOgAYQLo7=LOKzBcqzb8H7ZmAi0CokOIqqzfEvzxP4ejeFN6av9YrTl6pNKx8r5ZPpgryiV=o1wznNqZg+549zst8G+PeIQFyNLoQR2ayr+SovZC6Og310v6IbHH1wPtSnK1Fs0ekacb16MxPzaqoIVIoSr+175LrMTNjd8IOGDmsG8H5qT=qthhOYwGtiaruxtGWLoK=kWq4rnhwhmzyGDOeD6i0OBmT9QPQm5hm=m4DQIxGxDFqD+ODxD',
            'referer': 'https://www.taptap.com/app/7698/review',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
            'x-xsrf-token': 'eyJpdiI6ImI5M2JOZlJNak1mNjVRRVpibU9xdEE9PSIsInZhbHVlIjoiQ1wvOEM3VmRUd3phcyt6M1E1aXBhcHA4a0NDdkJyekp5T001SHBEbjlTOVI0Ykd4NndYZ0E2N1BhczFcL0N0Y1dWeVc2T2NTYmhwS29YZG1pUEhxMHE0Zz09IiwibWFjIjoiMjZlMzk0MjIxNGIyNjdjYjE4ZDQ1ODlkZWRkN2E3ZTA4NTgxYzMzM2E1YWY1OTliYWNiNzJiYTgzNzY0ODg1OSJ9'
        }
    #格式url链接，一条链接10个评论
    url = 'https://www.taptap.com/webapiv2/review/v2/by-app?app_id=227545&limit=10&from={}&X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D68%26VN%3D0.1.0%26LOC%3DCN%26PLT%3DPC%26DS%3DAndroid%26UID%3Deb1ddcd8-f82a-4372-a265-d4cc644572ce%26DT%3DPC%26OS%3DWindows%26OSV%3D10'
    urllist=[]
    for i in range(10):
        urllist.append(url.format(i))
    get_tap(urllist,headers)

