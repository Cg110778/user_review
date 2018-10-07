# -*- coding: utf-8 -*-
import pymongo
import re

import scrapy
from scrapy import Request,Spider

import scrapy

from douban5.items import *

class DoubanSpider(Spider):
    name = 'douban5'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/people/{uid}/']
    contacts_url= 'https://www.douban.com/people/{uid}/contacts'
    rev_contacts_url = 'https://www.douban.com/people/{uid}/rev_contacts'
    user_url = 'http://douban.com/people/{uid}/'
    start_users = ['128290489']#'57109633',#'1693422','50446886'ninetonine''137546285'183501886'#'3452208'新桥，宋史128290489
    movie_do_url = 'https://movie.douban.com/people/{uid}/do'
    movie_wish_url ='https://movie.douban.com/people/{uid}/wish'
    movie_collect_url ='https://movie.douban.com/people/{uid}/collect'
    music_do_url ='https://music.douban.com/people/{uid}/do'
    music_wish_url ='https://music.douban.com/people/{uid}/wish'
    music_collect_url ='https://music.douban.com/people/{uid}/collect'
    book_do_url ='https://book.douban.com/people/{uid}/do'
    book_wish_url ='https://book.douban.com/people/{uid}/wish'
    book_collect_url ='https://book.douban.com/people/{uid}/collect'
    contacts_id=[]
    movie_urls=[]
    music_urls=[]
    book_urls=[]
    movie_url = 'https://movie.douban.com/subject/{movieid}/'
    music_url = 'https://music.douban.com/subject/{musicid}/'
    book_url = 'https://book.douban.com/subject/{bookid}/'
    reviews_url='http://douban.com/people/{uid}/reviews'


    def get_id(self,collection, database):
        client = pymongo.MongoClient('localhost', 27017)
        db = client[database]
        collection = db[collection]
        #.skip(100)
        users_id= collection.find({},{'_id':0,'id':1}).limit(1).skip(150)
        return users_id

    def start_requests(self):
        for uid in self.start_users:
            yield Request(self.user_url.format(uid=uid), callback=self.parse_reviews)


    def parse_reviews(self,response):
        uids = self.get_id(collection='users', database='new_douban')
        for uid in uids:
            if uid:
                uid = uid['id']
                #print(uid)
                user_url=self.user_url.format(uid=uid)
                yield Request(url=self.reviews_url.format(uid=uid), meta={'user_url':user_url},callback=self.parse_reviews_detail)  # 用户长评



    def parse_reviews_detail(self,response):
        user_url=response.xpath(
            '//div[@class="review-list chart "]//div[@class="main review-item"]//header[@class="main-hd"]//a[@class="name"]/@href').extract_first()
        reviews=response.xpath(
            '//div[@class="review-list chart "]//div[@class="main review-item"]//div[@class="main-bd"]//h2/a/@href').extract()
        # 电影短评的直接链接列表
        #print(user_url)
        for review in reviews:
            print(review)
            if 'movie'in review:
               yield Request(url=review, callback=self.parse_movie_review)
            if 'music'in review:
               yield Request(url=review, callback=self.parse_music_review)
            if 'book'in review:
               yield Request(url=review, callback=self.parse_book_review)
            '''next_page = response.xpath(
                '//span[@class="next"]//a[contains(.,"后页")]/@href').extract_first()
            if next_page:
                next_page_url = str(user_url) + next_page
                # print(next_page,response.url)
                yield Request(url=next_page_url, callback=self.parse_reviews_detail)
                # 下一页reviews列表'''






    def parse_movie_review(self,response):
        item = DoubandetailmoviereviewItem()
        movie_review_url=response.url
        movie_id = response.xpath(
            '//*[@id="content"]//div[@class="subject-title"]/a/@href').extract_first()
        r_movie_id = re.search('.*?https://movie.douban.com/subject/(.*?)/.*?', movie_id)
        f_movie_id = r_movie_id.group(1)
        movie_reviewer_name = response.xpath(
            '//*[@id="content"]//div[@class="article"]//header[@class="main-hd"]//span[@property="v:reviewer"]/text()').extract_first()
        movie_reviewer_id = response.xpath(
            '//*[@id="content"]//div[@class="article"]//header[@class="main-hd"]/a').re_first(
            '<a href="https://www.douban.com/people/(.*?)/"')
        movie_reviewer_score = response.xpath(
            '//*[@id="content"]//div[@class="article"]//header[@class="main-hd"]/span').re_first(
            '<span class="allstar(\d+)0.*?</span>')
        movie_review_time = ''.join(response.xpath(
            '//*[@id="content"]//div[@class="article"]//header[@class="main-hd"]//span[@property="v:dtreviewed"]/text()').extract()).strip()
        movie_review_title = response.xpath(
            '//*[@id="content"]//div[@class="article"]//span[@property="v:summary"]/text()').extract_first()
        movie_review_content = ''.join(response.xpath(
            '//*[@id="content"]//div[@class="article"]//div[@class="main-bd"]//div[@property="v:description"]//text()').extract()).replace(
            '\n', '').strip()
        movie_review_useful_number = response.xpath(
            '//*[@id="content"]//div[@class="article"]//div[@class="main-ft"]//button/text()').re_first(
            '.*?有用 (\d+).*?')
        movie_review_useless_number = response.xpath(
            '//*[@id="content"]//div[@class="article"]//div[@class="main-ft"]//button/text()').re_first(
            '.*?没用 (\d+).*?')
        movie_review_info = [{'movie_reviewer_name': movie_reviewer_name, 'movie_reviewer_id': movie_reviewer_id,
                              'movie_reviewer_score': movie_reviewer_score, 'movie_review_time': movie_review_time,
                              'movie_review_title': movie_review_title, 'movie_review_content': movie_review_content,
                              'movie_review_useful_number': movie_review_useful_number,
                              'movie_review_useless_number': movie_review_useless_number}]
        item['movie_review_url']=movie_review_url
        item['movie_id'] = f_movie_id
        item['movie_review_info'] = movie_review_info
        yield item



    def parse_music_review(self,response):
        item = DoubandetailmusicreviewItem()
        music_review_url = response.url
        music_id = response.xpath(
            '//*[@id="content"]//div[@class="subject-title"]/a/@href').extract_first()
        r_music_id = re.search('.*?https://music.douban.com/subject/(.*?)/.*?', music_id)
        f_music_id = r_music_id.group(1)
        music_reviewer_name = response.xpath(
            '//*[@id="content"]//div[@class="article"]//header[@class="main-hd"]//span[@property="v:reviewer"]/text()').extract_first()
        music_reviewer_id = response.xpath(
            '//*[@id="content"]//div[@class="article"]//header[@class="main-hd"]/a').re_first(
            '<a href="https://www.douban.com/people/(.*?)/"')
        music_reviewer_score = response.xpath(
            '//*[@id="content"]//div[@class="article"]//header[@class="main-hd"]/span').re_first(
            '<span class="allstar(\d+)0.*?</span>')
        music_review_time = ''.join(response.xpath(
            '//*[@id="content"]//div[@class="article"]//header[@class="main-hd"]//span[@property="v:dtreviewed"]/text()').extract()).strip()
        music_review_title = response.xpath(
            '//*[@id="content"]//div[@class="article"]//span[@property="v:summary"]/text()').extract_first()
        music_review_content = ''.join(response.xpath(
            '//*[@id="content"]//div[@class="article"]//div[@class="main-bd"]//div[@property="v:description"]//text()').extract()).replace(
            '\n', '').strip()
        music_review_useful_number = response.xpath(
            '//*[@id="content"]//div[@class="article"]//div[@class="main-ft"]//button/text()').re_first(
            '.*?有用 (\d+).*?')
        music_review_useless_number = response.xpath(
            '//*[@id="content"]//div[@class="article"]//div[@class="main-ft"]//button/text()').re_first(
            '.*?没用 (\d+).*?')
        music_review_info = [{'music_reviewer_name': music_reviewer_name, 'music_reviewer_id': music_reviewer_id,
                              'music_reviewer_score': music_reviewer_score, 'music_review_time': music_review_time,
                              'music_review_title': music_review_title,
                              'music_review_content': music_review_content,
                              'music_review_useful_number': music_review_useful_number,
                              'music_review_useless_number': music_review_useless_number}]
        item['music_review_url'] = music_review_url
        item['music_id'] = f_music_id
        item['music_review_info'] = music_review_info
        yield item


    def parse_book_review(self,response):
        item = DoubandetailbookreviewItem()
        book_review_url = response.url
        book_id = response.xpath(
            '//*[@id="content"]//div[@class="subject-title"]/a/@href').extract_first()
        r_book_id = re.search('.*?https://book.douban.com/subject/(.*?)/.*?', book_id)
        f_book_id = r_book_id.group(1)
        book_reviewer_name = response.xpath(
            '//*[@id="content"]//div[@class="article"]//header[@class="main-hd"]//span[@property="v:reviewer"]/text()').extract_first()
        book_reviewer_id = response.xpath(
            '//*[@id="content"]//div[@class="article"]//header[@class="main-hd"]/a').re_first(
            '<a href="https://www.douban.com/people/(.*?)/"')
        book_reviewer_score = response.xpath(
            '//*[@id="content"]//div[@class="article"]//header[@class="main-hd"]/span').re_first(
            '<span class="allstar(\d+)0.*?</span>')
        book_review_time = ''.join(response.xpath(
            '//*[@id="content"]//div[@class="article"]//header[@class="main-hd"]//span[@property="v:dtreviewed"]/text()').extract()).strip()
        book_review_title = response.xpath(
            '//*[@id="content"]//div[@class="article"]//span[@property="v:summary"]/text()').extract_first()
        book_review_content = ''.join(response.xpath(
            '//*[@id="content"]//div[@class="article"]//div[@class="main-bd"]//div[@property="v:description"]//text()').extract()).replace(
            '\n', '').strip()
        book_review_useful_number = response.xpath(
            '//*[@id="content"]//div[@class="article"]//div[@class="main-ft"]//button/text()').re_first(
            '.*?有用 (\d+).*?')
        book_review_useless_number = response.xpath(
            '//*[@id="content"]//div[@class="article"]//div[@class="main-ft"]//button/text()').re_first(
            '.*?没用 (\d+).*?')
        book_review_info = [{'book_reviewer_name': book_reviewer_name, 'book_reviewer_id': book_reviewer_id,
                             'book_reviewer_score': book_reviewer_score, 'book_review_time': book_review_time,
                             'book_review_title': book_review_title,
                             'book_review_content': book_review_content,
                             'book_review_useful_number': book_review_useful_number,
                             'book_review_useless_number': book_review_useless_number}]
        item['book_review_url'] = book_review_url
        item['book_id'] = f_book_id
        item['book_review_info'] = book_review_info
        yield item


