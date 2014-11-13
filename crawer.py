#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2 
import os
import sys
import datetime
import uuid
from bs4 import BeautifulSoup

class Crawler(object):

    def crawl_html(self, url='http://www.ibeaconfans.com/?p=919'):
        content = urllib2.urlopen(url).read()
        return content	


class BlogParser(object):

    def __init__(self, content):
        self.content = BeautifulSoup(content)
        self.article = {}

    def __parse_article_head(self):
        header = self.content.find('h1', attrs = {'class': 'article-title'})
        self.article['title'] = header.next.text.encode('utf-8')
        #print self.article['title']

    def __parse_article_content(self):
        content_tag = self.content.find('article', attrs = {'class': 'article-content'})
        contents = content_tag.contents;
        contentsList = contents[1:len(contents) - 1]
        contentsList[-1].string = contentsList[-1].text.replace('请注明'.decode('utf-8'), '自'.decode('utf-8'))
        contentsStr = '\n'.join(['%s' % item.encode('utf-8') for item in contentsList])
        self.article['contents'] = contentsStr
        #print self.article['contents']

    def generate_post(self):
        self.__parse_article_head()
        self.__parse_article_content()
        today = datetime.date.today();
        timestr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        datestr = today.strftime('%Y-%m-%d')
        file_name = datestr + '-' + uuid.uuid1().get_hex() + '.markdown'
        with open('./_posts/' + file_name, 'w') as post_file:
            post_file.write('---\n')
            post_file.write('layout: post\n')
            post_file.write('title: "' + self.article['title'] + '"\n')
            post_file.write('date: ' + timestr + '\n')
            post_file.write('categories: indoorwise ibeacon\n')
            post_file.write('---\n')
            post_file.write(self.article['contents'])
        print 'file_name: ', file_name   

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 2:
        print 'please enter url for post!'         
    crawler = Crawler()
    content = crawler.crawl_html(args[1])

    parser = BlogParser(content)
    #parser.__parse_article_head()
    parser.generate_post()       
