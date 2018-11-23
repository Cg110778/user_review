# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field,Item
class DoubanuserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = 'users'
    id = Field()
    url=Field()
    name = Field()
    img = Field()
    habitual_residence = Field()  # 常居地
    record_date = Field()  # 注册日期
    user_display = Field()  # 用户信息展示
    contacts_count = Field()  # 关注人数
    rev_contacts_count = Field()
    movie_do_number=Field()
    movie_wish_number=Field()
    movie_collect_number=Field()
    music_do_number = Field()
    music_wish_number = Field()
    music_collect_number = Field()
    book_do_number = Field()
    book_wish_number = Field()
    book_collect_number = Field()

class UserRelationItem(Item):
    collection = 'users'
    id = Field()
    contacts = Field()  # 关注
    #rev_contacts = Field()

class DoubanMovietIdItem(Item):
    collection='users'
    id=Field()
    movie_id=Field()

class DoubanMusictIdItem(Item):
    collection = 'users'
    id = Field()
    music_id = Field()
class DoubanBookIdItem(Item):
    collection = 'users'
    id = Field()
    book_id = Field()

class DoubandetailmoviereviewItem(Item):
    collection = 'users'
    movie_review_url=Field()
    movie_id = Field()  # 电影id
    movie_review_info = Field()  # 影评
    movie_reviewer_name = Field()#影评者名称
    movie_reviewer_id = Field()#id
    movie_reviewer_score = Field()#星级
    movie_review_time = Field()#时间
    movie_review_title=Field() #标题
    movie_review_content= Field() #影评内容
    movie_review_useful_number = Field()  # 有用个数
    movie_review_useless_number = Field()  #无用个数




class DoubandetailmusicreviewItem(Item):
    collection = 'users'
    music_review_url=Field()
    music_id = Field()  # 音乐id
    music_review_info = Field()  # 乐评
    music_reviewer_name = Field()  # 乐评者名称
    music_reviewer_id = Field()  # id
    music_reviewer_score = Field()  # 星级
    music_review_time = Field()  # 时间
    music_review_title = Field()  # 标题
    music_review_content = Field()  # 乐评内容
    music_review_useful_number = Field()  # 有用个数
    music_review_useless_number = Field()  # 无用个数






class DoubandetailbookreviewItem(Item):
    collection = 'users'
    book_review_url=Field()
    book_id = Field()  # 书籍id
    book_review_info = Field()  # 书评
    book_reviewer_name = Field()  # 书评者名称
    book_reviewer_id = Field()  # id
    book_reviewer_score = Field()  # 星级
    book_review_time = Field()  # 时间
    book_review_title = Field()  # 标题
    book_review_content = Field()  # 书评内容
    book_review_useful_number = Field()  # 有用个数
    book_review_useless_number = Field()  # 无用个数













