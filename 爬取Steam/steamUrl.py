import random
import time
import requests
from bs4 import  BeautifulSoup
import os

#获取2个列表页HTML
def get_url(header,url,Htmlfile):
    if os.path.exists(Htmlfile)==False: #判断文件是否已经存在，防止重复爬取，导致ip被封禁
        steamtext=requests.get(url,headers=header).text
        steamtext=steamtext.replace("<!--","").replace("-->","") #对HTML文件去掉注释符合<!-- -->
        with open(Htmlfile,"w",encoding="utf-8") as f:
            f.write(steamtext)
        print(Htmlfile,'保存成功')
    else:
        print(Htmlfile,'已经存在！')

#解析出每个帖子的url
def get_link(Htmlfile):
    linklist=[]
    with open(Htmlfile, "r",encoding="utf-8") as f: #读取保存在本地的HTML文件
        html=f.read()
    #解析帖子url！
    soup=BeautifulSoup(html,"lxml")
    slist=soup.findAll("div", class_="threadlist_title pull_left j_th_tit")
    for i in slist:
        linklist.append(i.find("a")["href"])
    print("帖子链接列表",linklist)
    return linklist

def get_img(linklist,header):
    imglist=[]
    noImgnum=0
    for i in linklist:
        img_url="https://tieba.baidu.com"+i #拼接完整的帖子地址
        imgtext=requests.get(img_url,headers=header).text
        soup=BeautifulSoup(imgtext,'lxml')
        #获取帖子里面的图片，有一下帖子是没有图片的，相当于没有img标签，所以会报错，使用异常处理
        try :
            imglist.append(soup.find('img',class_='BDE_Image')["src"])
        except Exception as err:
            noImgnum+=1
    print("这页共有{}个图片,有{}个帖子没有图片".format(len(imglist),noImgnum))
    return imglist

def save_img(imglist,header,Htmlfile):
    #判断images文件夹是否存在，自动创建！
    os_path = os.getcwd() + '\\images\\'
    if os.path.exists(os_path) == False:
        os.mkdir(os_path)
        print("文件不存在，已新建images文件")
    else:
        print("文件已经存在不需要新建")
    #获取每个图片的二进制数据，并转存为图片，

    img_id=1
    for i in imglist:
        imgcont=requests.get(i,headers=header).content
        #拼接图片路径
        img_name=os_path+Htmlfile+str(img_id)+".jpg"
        print(Htmlfile+str(img_id)+".jpg","正在保存中...")
        with open(img_name,"wb+") as f:
            f.write(imgcont)
        img_id+=1

if __name__=="__main__":
    header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"}
    page=0
    page_in=eval(input("输入爬取的页数"))
    if page_in>20961:
        page_in=20961

    for i in range(page_in):
        time.sleep(random.randint(3,5))
        url="https://tieba.baidu.com/f?kw=steam&pn={}".format(page) #格式化帖子url
        Htmlfile = "steam{}.html".format(page)  #格式化帖子HTML文件名
        get_url(header,url,Htmlfile)
        getlink=get_link(Htmlfile)
        getimg=get_img(getlink,header)
        save_img(getimg,header,Htmlfile)
        page+=50