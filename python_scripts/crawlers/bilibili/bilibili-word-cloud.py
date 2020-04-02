#!/usr/bin/env python
# encoding: utf-8
'''
@author: Jerome
@file: bilibili-word-cloud.py
@time: 2019/10/27 12:19
@desc:
'''

from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from os import path
import jieba

# 1. 读取文件
# 2. 使用jieba生成词云
lj=path.dirname(__file__)   #当前文件路径
text=open(path.join(lj,'bilibili.txt'),encoding='utf-8').read() #读取的文本
jbText=' '.join(jieba.cut(text))
imgMask=np.array(Image.open(path.join(lj,'mask.jpeg')))   #读入背景图片
wc=WordCloud(
    background_color='white',
    max_words=500,
    font_path='msyh.ttc',    #默认不支持中文
    mask=imgMask,  #设置背景图片
    random_state=30 #生成多少种配色方案
).generate(jbText)
ImageColorGenerator(imgMask)   #根据图片生成词云颜色
# plt.imshow(wc)
# plt.axis('off')
# plt.show()
wc.to_file(path.join(lj,'biliDM.png'))
print('成功保存词云图片！')

