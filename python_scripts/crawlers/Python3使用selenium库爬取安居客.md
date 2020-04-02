# Python3使用selenium库爬取安居客
## 前言
某些网站为了反爬虫，可能会采取多种方式。比如，使用ajax技术异步加载数据、检测HTTP协议头信息等。当然，我们可以通过制作头信息，并提前找到实际数据的请求的URL路径。但这样就会存在许多问题，如：程序中会包含许多与程序本身逻辑的头信息，并且如果当每次需要寻找的数据的真实URL路径不同时，可能还需要再进行头信息的构造。这样，就会使得程序本身被大部分的头信息占据。
所以，为了解决这种问题，并且使得反爬取更加容易，selenium库出现了。它能够自动化操作浏览器进行点击、输入等人类一切可以在网页上完成的操作。由于selenium本身就是模拟人类去利用浏览器访问，所以使用selenium爬取数据时，就完全不用担心爬虫没有添加协议头信息以及实际请求数据与请求页面不相同的问题。
本文基于Chrome浏览器、Python3、pycharm、Chrome浏览器以及selenium，爬取了安居客在成都锦江区，价格在150-200万的部分二手房的信息。

## 安装selenium库以及Chrome driver
1. Chrome driver是用于selenium库自动化操作浏览器。不同浏览器，需要下载对应浏览器的driver。如Firefox需要下载Firefox driver。
2. selenium库安装
```
	pip3 install selenium
```
3. Chrome driver安装
    1. 首先下载Chrome driver的解压包,下载地址：<a href="http://npm.taobao.org/mirrors/chromedriver/">点这里</a>
    注意 ：chromedriver的版本要与你使用的chrome版本对应，对应关系如下：

    chromedriver版本|支持的Chrome版本
    :--:|:--:
    v2.33|v60-62
    v2.32|v59-61
    v2.31|v58-60
    v2.30|v58-60
    v2.29|v56-58
    v2.28|v55-57
    v2.27|v54-56
    v2.26|v53-55
    v2.25|v53-55
    v2.24|v52-54
    v2.23|v51-53
    v2.22|v49-52
    v2.21|v46-50
    v2.20|v43-48
    v2.19|v43-47
    v2.18|v43-46
    v2.17|v42-43
    v2.13|v42-45
    v2.15|v40-43
    v2.14|v39-42
    v2.13|v38-41
    v2.12|v36-40
    v2.11|v36-40
    v2.10|v33-36
    v2.9|v31-34
    v2.8|v30-33
    v2.7|v30-33
    v2.6|v29-32
    v2.5|v29-32
    v2.4|v29-32

    2. 将driver的exe文件放到Python的安装目录下，即安装成功
![driver](http://image.rainbowecho.top/driver.png)

## 关于seleniumAPI简单总结
selenium归根结底还是基于driver对网页进行爬取。所以，首先要做的就是获取到对应浏览器的driver对象。之后，在利用获取到的driver对象，进行元素选择、信息输入、表单提交、frame移动等复杂操作。本例只使用到了元素选择方面API，对于其他方面，在此不做讲解。毕竟，API还是要通过自己的阅读和使用才能熟练掌握。
1. 获取driver
使用Chrome浏览器就使用Chrome()方法，对应的，如果使用Firefox，就使用Firefox()
2. 元素选择
selenium的元素选择API类似于js的元素选择函数。如果读者对于利用js对DOM树中元素进行操作比较熟练的话，那么应该很容易理解这方面的API。只不过，selenium的元素选择API在选择的方式进行更多的扩展。如，可以使用css样式、xpath等方式进行选择。而选择器的写法，也与css选择器、xpath选择语法完全相同。读者完全可以放心使用。
3. 其他方面
既然是想要使用selenium库进行网页爬取的开发者，那么自然自身对于前端还是比较了解。比如类似表单如何完成，如何提交等。其实，另外这些方面的API也就是将用户实际的网页操作封装成了方法提供出来。所以，完全可以做到见文知义。这也是我没有再赘述的原因之一。如果是不清楚selenium库中有哪些API，有两种解决方法可供选择。一种是通过网上查找相关博客，有很多这方面的总结。另一种则是查看源码，直接查看库中API。

## 使用pycharm进行代码编写
```
import csv
import re

from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://chengdu.anjuke.com/sale/jinjiang/m58/')

house_links = browser.find_elements_by_css_selector('#houselist-mod-new a')
# 预存各个链接网址
hrefs = []
for link in house_links:
    hrefs.append(link.get_attribute('href'))

row_label = ['introduction', 'tags', 'saler']
data = []
for i in range(0, len(hrefs)):
    browser.get(hrefs[i])
    row = []

    if i == 0:
        labels = browser.find_elements_by_class_name('houseInfo-label')
        # 添加房屋细节label
        for label in labels:
            row_label.append(label.text)

    # 添加介绍列数据
    long_title = browser.find_element_by_class_name('long-title').text
    row.append(long_title)

    # 添加标签列数据
    tags = browser.find_elements_by_class_name('info-tag')
    tag_text = ''
    for tag in tags:
        # 去除HTML标签，合并tag
        tag_text += re.sub('<.*?>', '', tag.text)
        # 两个空白字符分隔不同tag
        tag_text += '  '

    row.append(tag_text)

    # 添加售卖者列数据
    owner = browser.find_element_by_class_name('brokercard-name').text
    row.append(owner)

    # 添加房屋所有详细列数据
    contents = browser.find_elements_by_class_name('houseInfo-content')
    for content in contents:
        row.append(content.text)

    data.append(row)
    print('第' + str(i+1) + '条房屋信息爬取完成')

print('开始写入文件')
# utf-8-sig避免中文乱码
with open('anjuke.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(row_label)
    writer.writerows(data)

print('文件写入完成')
browser.close()

```

## 实际爬取测试
1. 爬取效果：在程序中，没有采用多线程进行爬取，所以爬取网页速度较慢。
![anjuke1](http://image.rainbowecho.top/anjuke1.png)
![anjuke2](http://image.rainbowecho.top/anjuke2.png)
2. 数据展示（部分）：
![anjuke_data](http://image.rainbowecho.top/anjuke_data.png)
