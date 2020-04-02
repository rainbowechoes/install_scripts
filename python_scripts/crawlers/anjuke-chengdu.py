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