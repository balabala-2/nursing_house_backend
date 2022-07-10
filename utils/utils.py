import urllib.parse
import urllib.request
import time

#发送短信验证码
def send_verify_code(tel):
    # 接口地址
    url = 'http://106.ihuyi.com/webservice/sms.php?method=Submit'
    millis = int(round(time.time() * 100000))
    code = millis % 1000000
    # 定义请求的数据
    values = {
        'account': 'C74888128',
        'password': '67f123c9258474bb4663b3576b00d329',
        'mobile': str(tel),
        'content': '您的验证码是：' + str(code) +'。请不要把验证码泄露给其他人。',
        'format': 'json',
    }

    # 将数据进行编码
    data = urllib.parse.urlencode(values).encode(encoding='UTF8')

    # 发起请求
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    res = response.read()

    # 打印结果
    print(res.decode("utf8"))
    return str(code)