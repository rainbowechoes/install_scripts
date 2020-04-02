#!/usr/bin/env python
# encoding: utf-8
'''
@author: Jerome
@file: bilibili-comment.py
@time: 2019/10/27 12:13
@desc:
'''
import requests
import json

def str2obj(s, s1=';', s2='='):
    li = s.split(s1)
    res = {}
    for kv in li:
        li2 = kv.split(s2)
        if len(li2) > 1:
            res[li2[0]] = li2[1]
    return res

def crawlerHeader():
    headers = '''
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: application/json, text/plain, */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Referer: https://space.bilibili.com/4249401/video?tid=0&page=2&keyword=&order=pubdate
Cookie: LIVE_BUVID=AUTO1215721491866458; CURRENT_FNVAL=16; sid=5y1io4ai; stardustvideo=1
    '''
    headers = str2obj(headers, '\n', ': ')
    return headers

def getHTML(html, fi):
    # 页码
    count=1
    while(True):
        # json
        url=html+str(count)
        url=requests.get(url, headers = crawlerHeader())
        if url.status_code==200:
            content=json.loads(url.text)
            # 如果存在评论数据
            if content['data']['replies']:
                lengthRpy = len(content['data']['replies'])
                if count == 1:
                    try:
                        lengthHot = len(content['data']['hots'])
                        for i in range(lengthHot):
                            # 热门评论内容
                            hotMsg = content['data']['hots'][i]['content']['message']
                            fi.write(hotMsg + '\n')
                            leng = len(content['data']['hots'][i]['replies'])
                            for j in range(leng):
                                # 热门评论回复内容
                                hotMsgRp = content['data']['hots'][i]['replies'][j]['content']['message']
                                fi.write(hotMsgRp + '\n')
                    except:
                        pass
                if lengthRpy != 0:
                    for i in range(lengthRpy):
                        replyItem = content['data']['replies'][i]
                        comMsg = replyItem['content']['message']
                        fi.write(comMsg + '\n')
                        print('\t评论:', comMsg)
                        if replyItem['replies']:
                            leng = len(replyItem['replies'])
                            for j in range(leng):
                                comMsgRp = replyItem['replies'][j]['content']['message']
                                fi.write(comMsgRp + '\n')
                                print('\t\t回复:' + comMsgRp)
                else:
                    break
                print("\t评论第%d页写入成功！" % count)
                count += 1
            else:
                print('该视频评论数据已爬取完成')
                break
        else:
            print('视频评论信息爬取异常，提前结束')
            break

# 对txt内容还进行简单的内容过滤 1. 回复词 2. 表情符号
def getVideo():
    page = 1
    fi=open('bilibili.txt','w',encoding='utf-8')
    while(True):
        #  api
        spaceUrl = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=4249401&pagesize=30&tid=0&page=' + str(page) +'&keyword=&order=pubdate'
        crawlResult = requests.get(spaceUrl, headers = crawlerHeader())
        if crawlResult.status_code == 200:
            videoContent = json.loads(crawlResult.text)
            if videoContent['data']['vlist']:
                videoList = videoContent['data']['vlist']
                for videoItem in videoList:
                    videoId = videoItem['aid']
                    print('将要爬取视频：' + videoItem['title'])
                    commentUrl = "https://api.bilibili.com/x/v2/reply?type=1&oid="
                    html = commentUrl + str(videoId) + '&pn='
                    getHTML(html, fi)
                page += 1
            else:
                print('视频已爬取完成')
                break
        else:
            print('视频列表爬取异常，提前结束')
            break
    fi.close()


if __name__ == '__main__':
    getVideo()
