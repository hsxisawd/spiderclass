import requests
import hashlib,time,random

def md5_sgin(text):
    hl=hashlib.md5()
    sgin_text='6key_cibaifanyicjbysdlove1'+text
    hl.update(sgin_text.encode(encoding='utf-8'))
    sign=hl.hexdigest()[0:16]
    return sign,text

def fanyi(sign,text,ol,nl):
    url=f"http://ifanyi.iciba.com/index.php?c=trans&m=fy&client=6&auth_user=key_ciba&sign={sign}"
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}
    p={'from': ol,'to': nl,'q': text}
    time.sleep(random.randint(1,2))
    js_data=requests.post(url,data=p,headers=header).json()
    print(f"翻译结果:{js_data['content']['out']} || [{js_data['content']['ciba_use']}]")


if __name__=="__main__":
    print("zh=中文,en=英语,fr=法语,ja=日语,ko=韩语,de=德语,es=西班牙语")
    oldlanguage=input("选择要翻译的语种!")
    text=input('输入要翻译的文本！')
    newlanguage=input("选择翻译成什么语言！")
    a,b=md5_sgin(text)
    fanyi(a,b,oldlanguage,newlanguage)