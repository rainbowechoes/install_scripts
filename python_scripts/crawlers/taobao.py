import requests
import re
import pymysql
# from redis import StrictRedis, ConnectionPool


def str2obj(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            res[li2[0]] = li2[1]
    return res


db = pymysql.connect(host='localhost', port=3306, user='root', password='root', db='cake')
cursor = db.cursor()
id = 1
goods_list = ['服装鞋包', '日用品', '美妆', '家电']
for category in range(0, 4):
    goods = goods_list[category]
    # page = 1
    for page in range(1, 8):
        url = 'https://s.taobao.com/search?q=' + goods + '&s=' + str(page * 44)
        headers = '''
GET /search?q=%E5%8F%B0%E5%BC%8F%E7%94%B5%E8%84%91&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=3&ntoffset=3&p4ppushleft=1%2C48&s=88 HTTP/1.1
Host: s.taobao.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: t=d4898120c6274e92b0556c405ef029a7; cna=5+xWFWnfjUUCAbaVaXVLsHYP; isg=BHx8idJbDNJd3zgAvG7fv4t-ThokeGXThA6iQFb9iGdKIRyrfoXwL_KTBY_8clj3; l=bBr-f20rv0ebpNioBOCNZZ9_WibtLIOYYuWf5X4Hi_5Cg6Y_KL_Olp94IFv6V_CR_tYB4RVd54p9-etki; cookie2=13952771926e07c6b1ce56d5874e5ea8; v=0; _tb_token_=35e3b331e3b6f; unb=2959453891; uc1=cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&existShop=false&pas=0&cookie14=UoTZ48xqXx5D4A%3D%3D&tag=8&lng=zh_CN; sg=%E8%B4%BC15; _l_g_=Ug%3D%3D; skt=147c4c7e78389d09; cookie1=B0Sr4OvXD9MUHEBR6zQ5v8fI3e3Ns11WWmf3aDpMkyo%3D; csg=2f7d5a42; uc3=vt3=F8dBy3qOP7Mennyc%2BTQ%3D&id2=UUGnwzxLCx8RfA%3D%3D&nk2=saCh9ehIgciFVQ%3D%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D; existShop=MTU1Nzk5MTM3NA%3D%3D; tracknick=%5Cu4E00%5Cu4E2A%5Cu5C0F%5Cu7A83%5Cu8D3C; lgc=%5Cu4E00%5Cu4E2A%5Cu5C0F%5Cu7A83%5Cu8D3C; _cc_=U%2BGCWk%2F7og%3D%3D; dnk=%5Cu4E00%5Cu4E2A%5Cu5C0F%5Cu7A83%5Cu8D3C; _nk_=%5Cu4E00%5Cu4E2A%5Cu5C0F%5Cu7A83%5Cu8D3C; cookie17=UUGnwzxLCx8RfA%3D%3D; tg=0; mt=ci=113_1; enc=ibue7ZnBunlpygyaU7akpGLPdAG9QNLRQHDoqzZo1eMKhR8%2BsxJyNHY3Hm1MveoHk%2BAlKBjB%2FRswMIWAkLDiVg%3D%3D; JSESSIONID=FC9625143E5BE763E18E3A674FA0E7BE; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; swfstore=178300; whl=-1%260%260%260
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
        '''
        headers = str2obj(headers, '\n', ': ')

        # pool = ConnectionPool(host='localhost', port=6379, db=0)
        # redis = StrictRedis(connection_pool=pool)

        html_data = requests.get(url, headers=headers, timeout=10).text
        data_text = re.findall('g_page_config = \{.*?};', html_data)[0]
        title_list = re.findall('"raw_title":"(.*?)"', data_text)
        price_list = re.findall('"view_price":"(.*?)"', data_text)
        pic_list = re.findall('"pic_url":"(.*?)"', data_text)
        location_list = re.findall('"item_loc":"(.*?)"', data_text)
        sales_list = re.findall('"view_sales":"(.*?)"', data_text)
        nick_list = re.findall('"nick":"(.*?)"', data_text)

        row_label = ['nick', 'location', 'sales', 'price', 'title', 'pic']
        sql = 'insert into goods(id, `name`, cover, price, intro, stock, type_id) values (%s, %s, %s, %s, %s, %s, %s);'
        for i in range(len(sales_list)):
            cursor.execute(sql, (id, title_list[i], pic_list[i], price_list[i], title_list[i], 120, category))
            id = id + 1

db.commit()
db.close()
