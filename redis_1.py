# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 17:19:24 2018

@author: Administrator
"""

import urllib
import urllib.request as urllib2
import re
import threading
import time


'''
url = 'http://www.qiushibaike.com/hot/page/1'

headers1={
     'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
}
#构建请求的request
request = urllib2.Request(url,headers = headers1)
#利用urlopen获取页面代码
response = urllib2.urlopen(request)
#将页面转化为UTF-8编码
pageCode = response.read().decode('utf-8')




pattern = re.compile('<div class="author clearfix">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?'+
                         'content">(.*?).*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)

pattern1 = re.compile('<div class="author clearfix">.*?<a.*?<img.*?>.*?<div class="content">.*?class="number">',re.S)

pattern2 = re.compile('<div class="content">.*?<span>(.*?)</span>',re.S)


items = re.findall(pattern2,pageCode)

print(items)


#用来存储每页的段子们
pageStories = []
#遍历正则表达式匹配的信息
for item in items:
    replaceBR = re.compile('<br/>')
    text = re.sub(replaceBR,"\n",item)
    pageStories.append([text.strip()])

print(pageStories)


'''


#糗事百科爬虫类
class QSBK:
 
    #初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        #初始化headers
        self.headers = {
     'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
}
        #存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        #存放程序是否继续运行的变量
        self.enable = False
    #传入某一页的索引获得页面代码
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            #构建请求的request
            request = urllib2.Request(url,headers = self.headers)
            #利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            #将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError as e:
            if hasattr(e,"reason"):
                print("连接糗事百科失败,错误原因",e.reason)
                return None
 
 
    #传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print ("页面加载失败....")
            return None
        pattern = re.compile('<div.*?author">.*?<a.*?<img.*?>(.*?)</a>.*?<div.*?'+
                         'content">(.*?)<!--(.*?)-->.*?</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
        pattern2 = re.compile('<div class="content">.*?<span>(.*?)</span>',re.S)
        items = re.findall(pattern2,pageCode)
        #用来存储每页的段子们
        pageStories = []
        #遍历正则表达式匹配的信息
        for item in items:
            replaceBR = re.compile('<br/>')
            text = re.sub(replaceBR,"\n",item)
            pageStories.append([text.strip()])
        return pageStories
 
    #加载并提取页面的内容，加入到列表中
    def loadPage(self):
        #如果当前未看的页数少于2页，则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                #获取新一页
                pageStories = self.getPageItems(self.pageIndex)
                #将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    #获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1
    
    #调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self,pageStories,page):
        #遍历一页的段子
        for story in pageStories:
            #等待用户输入
            input = 'a'
            #每当输入回车一次，判断一下是否要加载新页面
            
            self.loadPage()
            #如果输入Q则程序结束
            if input == "Q":
                self.enable = False
                return
            print ("第%d页\t\n%s" %(page,story[0]))
    
    #开始方法
    def start(self):
        print ("正在读取糗事百科,按回车查看新段子，Q退出")
        #使变量为True，程序可以正常运行
        self.enable = True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前读到了第几页
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                #从全局list中获取一页的段子
                pageStories = self.stories[0]
                #当前读到的页数加一
                nowPage += 1
                #将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)
 

spider = QSBK()
spider.start()
