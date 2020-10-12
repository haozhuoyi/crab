# crab
公司发的大闸蟹礼品卡，怎么都预约不上，于是写了个脚本，自己记录用

## 利用讯飞api识别验证码

``` bash

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
