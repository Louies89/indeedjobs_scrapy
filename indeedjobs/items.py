# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IndeedJobsItem(scrapy.Item):
    # define the fields for your item here
    job_page_index = scrapy.Field()            #Page index where the job was found
    job_id = scrapy.Field()                    #Internal Id for storing the job post
    job_title = scrapy.Field()                 #Title of the Job Posted
    job_location = scrapy.Field()              #Job Location
    job_company = scrapy.Field()               #Company Name
    job_company_rating = scrapy.Field()        #Company Rating if availble 
    job_postedon = scrapy.Field()              #Job Posted On
    job_salary = scrapy.Field()                #Salary/Salary Range
    job_type = scrapy.Field()                  #Full Time/Part Time/Contract
    job_description_link = scrapy.Field()      #Link to the job description
    job_description = scrapy.Field()           #Job Description
    job_postedonsites = scrapy.Field()         #All sites where the job is posted
    job_sitelinks = scrapy.Field()             #Link to the job Post
    job_company_logo_link = scrapy.Field()     # Logo of the company