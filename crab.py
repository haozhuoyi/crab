import requests
import time
import hashlib
import base64
import json
import os
import json
from PIL import Image
from io import BytesIO

def main():
    cardId = ''
    password = ''
    userName = ''
    phonenum = ''
    address = ''

    # 获取cookie
    cookie = getCookie()
    # 获取验证码
    veriCode = getVeriCode(cookie)
    # 字节流转png
    veriCodeImg = veriCodeDecode(veriCode)
    # 识别png(讯飞api)
    veriCodeNum = VeriCodeDis(veriCodeImg)
    # 登录
    login(cardId,password,veriCodeNum,cookie)
    # 提货
    # getCrab(userName,phonenum,address,veriCodeNum,cookie)

def getCookie():
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'hab.360xie.cn',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    url = 'http://hab.360xie.cn/'
    response = requests.get(url,  headers = header)
    response.encoding = 'utf-8'
    cookie = response.headers['Set-Cookie']
    print (response.headers['Set-Cookie'])
    return cookie


def getVeriCode(cookie):
    header = {
        'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
        'Cache-Control': 'no-cache',
        'Cookie':cookie,
        'Connection': 'keep-alive',
        'Host': 'hab.360xie.cn',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    url = 'http://hab.360xie.cn/ucControl/rand.ashx'
    response = requests.get(url,  headers = header)
    print (response.content)
    return response.content


def veriCodeDecode(veriCode):
    #将bytes结果转化为字节流
    bytes_stream = BytesIO(veriCode)
    #读取到图片
    veriCodeImg = Image.open(bytes_stream)

    imgByteArr = BytesIO()    #初始化一个空字节流
    veriCodeImg.save(imgByteArr,format('PNG'))     #把我们得图片以‘PNG’保存到空字节流
    imgByteArr = imgByteArr.getvalue()    #无视指针，获取全部内容，类型由io流变成bytes。
    with open('./abc.png','wb') as f:
        f.write(imgByteArr)
    return veriCodeImg
    # roiimg.show()  #展示图片


def VeriCodeDis(veriCodeImg):
    # 印刷文字识别 webapi 接口地址
    URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/general"
    # 应用ID
    APPID = ""
    # 接口密钥
    API_KEY = ""
    def getHeader():
    #  当前时间戳
        curTime = str(int(time.time()))
    #  支持语言类型和是否开启位置定位(默认否)
        param = {"language": "cn|en", "location": "false"}
        param = json.dumps(param)
        paramBase64 = base64.b64encode(param.encode('utf-8'))

        m2 = hashlib.md5()
        str1 = API_KEY + curTime + str(paramBase64,'utf-8')
        m2.update(str1.encode('utf-8'))
        checkSum = m2.hexdigest()
    # 组装http请求头
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': APPID,
            'X-CheckSum': checkSum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header
    # 上传文件并进行base64位编码
    with open(r'./abc.png', 'rb') as f:
        f1 = f.read()

    f1_base64 = str(base64.b64encode(f1), 'utf-8')


    data = {
            'image': f1_base64
            }


    r = requests.post(URL, data=data, headers=getHeader())
    result = str(r.content, 'utf-8')
    # 错误码链接：https://www.xfyun.cn/document/error-code (code返回错误码时必看)
    print(result)
    resultAry = json.loads(result)
    # input("Entry the any key to exit")
    veriCodeNum = resultAry['data']['block'][0]['line'][0]['word'][0]['content']
    print(veriCodeNum)
    return veriCodeNum

def login(cardId,password,veriCodeNum,cookie):
    header = {
        'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
        'Cache-Control': 'no-cache',
        'Cookie':cookie,
        'Connection': 'keep-alive',
        'Host': 'hab.360xie.cn',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    data = {
        '__VIEWSTATE': '/wEPDwUJMjUzODMyMzcxD2QWAgIDD2QWBgIFDxYCHgRUZXh0BeYG5bCK5pWs55qE6aG+5a6i5oKo5aW9PGJyIC8+MeOAgeWPkei0p++8muS4gOe6v+WfjuW4gjQ45bCP5pe26YCB6L6+77yM5YGP6L+c5Zyw5Yy65bu26L+fMi0z5aSp77ybPGJyIC8+MuOAgemihOe6pu+8mumihOe6puaXtumXtOS4uuWPkei0p+aXtumXtO+8jOS4jeaYr+mAgeWIsOaXtumXtO+8m+S4jeiDvemihOe6puW9k+WkqeWPkei0p++8jOWPquiDveS7juesrOS4ieWkqeW8gOWni+e6pu+8mzxiciAvPjPjgIHmn6XnnIvvvJrovpPlhaXljaHlj7fjgIHlr4bnoIHlj6/ku6Xmn6XnnIvpooTnuqbmmK/lkKbmiJDlip/vvJsgPGJyIC8+NOOAge+8iOWboOesrOS4ieaWueW/q+mAkumFjemAge+8jOWPl+WkqeawlOOAgeiIquePreOAgeiKguaXpeeIhuS7k+etieS4jeWPr+aKl+WboOe0oOW9seWTje+8jOS8mumAoOaIkOW7tui/n++8jOivt+azqOaEj+i3n+i4qumFjemAgei/m+eoi++8m++8iTxiciAvPjXjgIHnlJ/pspzpo5/lk4Hlj5HotKflkI7kuI3lj6/mm7TmlLnmlLbku7blnLDlnYDvvIzor7fkv53mjIHnlLXor53nlYXpgJrvvIzlrrbkuK3nlZnkurrnrb7mlLbjgII8YnIgLz7llYblrrbmuKnppqjmj5DnpLrvvJoxMOaciOS4reaXrOaYr+acgOS9s+Wkp+mXuOifueWTgeifueWto+iKgu+8jOW7uuiuruWkp+WutjEw5pyI6aKE57qm5o+Q6LSn77yM6J+56buE5pu05Yqg6aWx5ruh77yM5Y+j5oSf5pyA5L2z44CC6K+35oKo5LuU57uG5qC45a+55L+h5oGv77ybPGJyIC8+IOaEn+iwouaCqOeahOeQhuino+S4jumFjeWQiO+8gTxiciAvPua4qemmqOaPkOekuu+8muS7iuWkqemAmumBk+abtOaWsOe7k+adn++8jOivt+aMgee7reWFs+azqOWFrOS8l+WPt++8jOavj+aXpTEy54K55Lya6Ieq5Yqo5pu05paw5o+Q6LSn5pel5pyf44CCZAIGD2QWBGYPFgIfAAUh6IuP5bee5biC6IuP5rOi6J+55Lia5pyJ6ZmQ5YWs5Y+4ZAIBDxYCHwAFCzE4OTYzNjcyMDg3ZAIHDxYCHwAF5gblsIrmlaznmoTpob7lrqLmgqjlpb08YnIgLz4x44CB5Y+R6LSn77ya5LiA57q/5Z+O5biCNDjlsI/ml7bpgIHovr7vvIzlgY/ov5zlnLDljLrlu7bov58yLTPlpKnvvJs8YnIgLz4y44CB6aKE57qm77ya6aKE57qm5pe26Ze05Li65Y+R6LSn5pe26Ze077yM5LiN5piv6YCB5Yiw5pe26Ze077yb5LiN6IO96aKE57qm5b2T5aSp5Y+R6LSn77yM5Y+q6IO95LuO56ys5LiJ5aSp5byA5aeL57qm77ybPGJyIC8+M+OAgeafpeeci++8mui+k+WFpeWNoeWPt+OAgeWvhueggeWPr+S7peafpeeci+mihOe6puaYr+WQpuaIkOWKn++8myA8YnIgLz4044CB77yI5Zug56ys5LiJ5pa55b+r6YCS6YWN6YCB77yM5Y+X5aSp5rCU44CB6Iiq54+t44CB6IqC5pel54iG5LuT562J5LiN5Y+v5oqX5Zug57Sg5b2x5ZON77yM5Lya6YCg5oiQ5bu26L+f77yM6K+35rOo5oSP6Lef6Liq6YWN6YCB6L+b56iL77yb77yJPGJyIC8+NeOAgeeUn+mynOmjn+WTgeWPkei0p+WQjuS4jeWPr+abtOaUueaUtuS7tuWcsOWdgO+8jOivt+S/neaMgeeUteivneeVhemAmu+8jOWutuS4reeVmeS6uuetvuaUtuOAgjxiciAvPuWVhuWutua4qemmqOaPkOekuu+8mjEw5pyI5Lit5pes5piv5pyA5L2z5aSn6Ze46J+55ZOB6J+55a2j6IqC77yM5bu66K6u5aSn5a62MTDmnIjpooTnuqbmj5DotKfvvIzon7npu4Tmm7TliqDppbHmu6HvvIzlj6PmhJ/mnIDkvbPjgILor7fmgqjku5Tnu4bmoLjlr7nkv6Hmga/vvJs8YnIgLz4g5oSf6LCi5oKo55qE55CG6Kej5LiO6YWN5ZCI77yBPGJyIC8+5rip6aao5o+Q56S677ya5LuK5aSp6YCa6YGT5pu05paw57uT5p2f77yM6K+35oyB57ut5YWz5rOo5YWs5LyX5Y+377yM5q+P5pelMTLngrnkvJroh6rliqjmm7TmlrDmj5DotKfml6XmnJ/jgIJkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQlidG5TZWFyY2gEnA90oljKwqUdwJ+kUmEdLKr83+PRURqUvDfy2YMo9Q==',
        '__EVENTVALIDATION': '/wEdAAYJY9DOztdSQ6lIb+rhkw1R5OUu0LPCoZYiiL5gmnf1pRSZj6OW6PHu+FpQ8A+MtQZyS2f5c1XgBSx3nGmY/9ewjtTdVzRZn7DFyWrI8V/OY650TeJsEoMHpRWXyCCjB/AMPngfaAUs/BZlqODhBk+WVeYsYnOoYT0HViq0b+1yiA==',
        'txtCardNo': cardId,
        'txtCardPsw': password,
        'txtValidate': veriCodeNum,
        'btnSearch.x': '131',
        'btnSearch.y': '40',
        'footer1$hideMercid': '253'
    }
    url = 'http://hab.360xie.cn/'
    response = requests.post(url, headers = header, data = data)
    print (response.content.decode("utf-8"))

def getCrab(userName,phonenum,address,veriCodeNum,cookie):
    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
        'Cache-Control': 'no-cache',
        'Content-Length': '5676',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':cookie,
        'Origin': 'http://hab.360xie.cn',
        'Referer': 'http://hab.360xie.cn/inputinfo.aspx?validate=' + veriCodeNum + '&mercid=253',
        'X-MicrosoftAjax': 'Delta=true',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Host': 'hab.360xie.cn',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    data = {
        'ScriptManager1': 'UpdatePanel4|btnAdd',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': '/wEPDwUJMjUzODMyMzcxD2QWAgIDD2QWBgIFDxYCHgRUZXh0BeYG5bCK5pWs55qE6aG+5a6i5oKo5aW9PGJyIC8+MeOAgeWPkei0p++8muS4gOe6v+WfjuW4gjQ45bCP5pe26YCB6L6+77yM5YGP6L+c5Zyw5Yy65bu26L+fMi0z5aSp77ybPGJyIC8+MuOAgemihOe6pu+8mumihOe6puaXtumXtOS4uuWPkei0p+aXtumXtO+8jOS4jeaYr+mAgeWIsOaXtumXtO+8m+S4jeiDvemihOe6puW9k+WkqeWPkei0p++8jOWPquiDveS7juesrOS4ieWkqeW8gOWni+e6pu+8mzxiciAvPjPjgIHmn6XnnIvvvJrovpPlhaXljaHlj7fjgIHlr4bnoIHlj6/ku6Xmn6XnnIvpooTnuqbmmK/lkKbmiJDlip/vvJsgPGJyIC8+NOOAge+8iOWboOesrOS4ieaWueW/q+mAkumFjemAge+8jOWPl+WkqeawlOOAgeiIquePreOAgeiKguaXpeeIhuS7k+etieS4jeWPr+aKl+WboOe0oOW9seWTje+8jOS8mumAoOaIkOW7tui/n++8jOivt+azqOaEj+i3n+i4qumFjemAgei/m+eoi++8m++8iTxiciAvPjXjgIHnlJ/pspzpo5/lk4Hlj5HotKflkI7kuI3lj6/mm7TmlLnmlLbku7blnLDlnYDvvIzor7fkv53mjIHnlLXor53nlYXpgJrvvIzlrrbkuK3nlZnkurrnrb7mlLbjgII8YnIgLz7llYblrrbmuKnppqjmj5DnpLrvvJoxMOaciOS4reaXrOaYr+acgOS9s+Wkp+mXuOifueWTgeifueWto+iKgu+8jOW7uuiuruWkp+WutjEw5pyI6aKE57qm5o+Q6LSn77yM6J+56buE5pu05Yqg6aWx5ruh77yM5Y+j5oSf5pyA5L2z44CC6K+35oKo5LuU57uG5qC45a+55L+h5oGv77ybPGJyIC8+IOaEn+iwouaCqOeahOeQhuino+S4jumFjeWQiO+8gTxiciAvPua4qemmqOaPkOekuu+8muS7iuWkqemAmumBk+abtOaWsOe7k+adn++8jOivt+aMgee7reWFs+azqOWFrOS8l+WPt++8jOavj+aXpTEy54K55Lya6Ieq5Yqo5pu05paw5o+Q6LSn5pel5pyf44CCZAIGD2QWBGYPFgIfAAUh6IuP5bee5biC6IuP5rOi6J+55Lia5pyJ6ZmQ5YWs5Y+4ZAIBDxYCHwAFCzE4OTYzNjcyMDg3ZAIHDxYCHwAF5gblsIrmlaznmoTpob7lrqLmgqjlpb08YnIgLz4x44CB5Y+R6LSn77ya5LiA57q/5Z+O5biCNDjlsI/ml7bpgIHovr7vvIzlgY/ov5zlnLDljLrlu7bov58yLTPlpKnvvJs8YnIgLz4y44CB6aKE57qm77ya6aKE57qm5pe26Ze05Li65Y+R6LSn5pe26Ze077yM5LiN5piv6YCB5Yiw5pe26Ze077yb5LiN6IO96aKE57qm5b2T5aSp5Y+R6LSn77yM5Y+q6IO95LuO56ys5LiJ5aSp5byA5aeL57qm77ybPGJyIC8+M+OAgeafpeeci++8mui+k+WFpeWNoeWPt+OAgeWvhueggeWPr+S7peafpeeci+mihOe6puaYr+WQpuaIkOWKn++8myA8YnIgLz4044CB77yI5Zug56ys5LiJ5pa55b+r6YCS6YWN6YCB77yM5Y+X5aSp5rCU44CB6Iiq54+t44CB6IqC5pel54iG5LuT562J5LiN5Y+v5oqX5Zug57Sg5b2x5ZON77yM5Lya6YCg5oiQ5bu26L+f77yM6K+35rOo5oSP6Lef6Liq6YWN6YCB6L+b56iL77yb77yJPGJyIC8+NeOAgeeUn+mynOmjn+WTgeWPkei0p+WQjuS4jeWPr+abtOaUueaUtuS7tuWcsOWdgO+8jOivt+S/neaMgeeUteivneeVhemAmu+8jOWutuS4reeVmeS6uuetvuaUtuOAgjxiciAvPuWVhuWutua4qemmqOaPkOekuu+8mjEw5pyI5Lit5pes5piv5pyA5L2z5aSn6Ze46J+55ZOB6J+55a2j6IqC77yM5bu66K6u5aSn5a62MTDmnIjpooTnuqbmj5DotKfvvIzon7npu4Tmm7TliqDppbHmu6HvvIzlj6PmhJ/mnIDkvbPjgILor7fmgqjku5Tnu4bmoLjlr7nkv6Hmga/vvJs8YnIgLz4g5oSf6LCi5oKo55qE55CG6Kej5LiO6YWN5ZCI77yBPGJyIC8+5rip6aao5o+Q56S677ya5LuK5aSp6YCa6YGT5pu05paw57uT5p2f77yM6K+35oyB57ut5YWz5rOo5YWs5LyX5Y+377yM5q+P5pelMTLngrnkvJroh6rliqjmm7TmlrDmj5DotKfml6XmnJ/jgIJkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQlidG5TZWFyY2gEnA90oljKwqUdwJ+kUmEdLKr83+PRURqUvDfy2YMo9Q==',
        '__EVENTVALIDATION': '/wEdAAYJY9DOztdSQ6lIb+rhkw1R5OUu0LPCoZYiiL5gmnf1pRSZj6OW6PHu+FpQ8A+MtQZyS2f5c1XgBSx3nGmY/9ewjtTdVzRZn7DFyWrI8V/OY650TeJsEoMHpRWXyCCjB/AMPngfaAUs/BZlqODhBk+WVeYsYnOoYT0HViq0b+1yiA==',
        'txtCardName': '2019阳澄绿色大闸蟹1998型礼卡',
        'txtStateSell': '此卡已售',
        'txtStateGet': '可以提货',
        'txtBegin': '2019-07-12',
        'txtEnd': '2020-12-31',
        'txtName': userName,
        'txtTele': phonenum,
        'txtTeleBak': '',
        'ddlSheng': '15',
        'ddlShi': '1400',
        'ddlQu': '1424',
        'txtAddr1': address,
        'ddlDate': '2020-10-11',
        'footer1$hideMercid': '253',
        '__ASYNCPOST': 'true',
        'btnAdd.x': '148',
        'btnAdd.y': '26'
    }
    url = 'http://hab.360xie.cn/inputinfo.aspx?validate=' + veriCodeNum + '&mercid=253'
    response = requests.post(url, headers = header, data = data)
    print (response.content.decode("utf-8"))


if __name__ == '__main__':
    main()
