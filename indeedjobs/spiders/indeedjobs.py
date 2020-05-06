import scrapy
from ..items import IndeedJobsItem
import time
import html2text
import hashlib

def current_milli_time(): return int(round(time.time() * 1000))


# Command to Run : 
# 1. scrapy crawl indeedjobs -a category='Python' -a location='India'
# 1. scrapy crawl indeedjobs -a category='Python Data Science' -a location='India'

class IndeedJobs(scrapy.Spider):
    name = 'indeedjobs'
    
    def __init__(self, category='elixir', location='India', *args, **kwargs):
        super(IndeedJobs, self).__init__(*args, **kwargs)
        self.start_urls = [
                # 'https://www.google.com/search?q=Python+jobs&ibp=htl;jobs'
                # 'https://www.indeed.co.in/jobs?q=Python&l=India'
                # 'https://www.indeed.co.in/jobs?q=elixir&l=India'
                f'https://www.indeed.co.in/jobs?q={category}&l={location}'
            ]

    page_index = 1
    force_load_count = 0

    def parse(self, response):
        self.logger.info(f'-------------Parse function called on {response.url}')
        jobInfo = IndeedJobsItem()

        # return a array of results
        job_list = response.css("div.jobsearch-SerpJobCard.unifiedRow.row.result")

        for job in job_list:
            # print(job)
            try:
                
                # Get Job Title (https://stackoverflow.com/questions/21181628/get-href-using-css-selector-with-scrapy)
                job_title = job.css("h2").css("a::attr(title)")
                if(job_title):
                    jobInfo['job_title'] = job_title[0].get().strip()
                else:
                    jobInfo['job_title'] = ''

                # Get Job Location
                job_location = job.css("span.location.accessible-contrast-color-location::text")
                if(job_location):
                    jobInfo['job_location'] = job_location[0].get().strip()
                else:
                    jobInfo['job_location'] = ''

                # Get Company Name
                job_company = job.css("div").css("span.company::text")
                if(job_company):
                    jobInfo['job_company'] = job_company[0].get().strip()
                else:
                    jobInfo['job_company'] = ''

                # Get Rating of the Company
                job_company_rating = job.css("span.ratingsContent::text")
                if(job_company_rating):
                    jobInfo['job_company_rating'] = job_company_rating[0].get().strip()
                else:
                    jobInfo['job_company_rating'] = ''

                # Get job posted time
                job_postedon = job.css("div.jobsearch-SerpJobCard-footer").css("div.result-link-bar").css("span.date::text")
                if(job_postedon):
                    jobInfo['job_postedon'] = {'scrapedon': current_milli_time(), 'postedon': job_postedon[0].get().strip()}
                else:
                    jobInfo['job_postedon'] = ''

                # Get job salary
                job_salary = job.css("div.salarySnippet.salarySnippetDemphasizeholisticSalary").css("span.salaryText::text")
                if(job_salary):
                    jobInfo['job_salary'] = job_salary[0].get().strip()
                else:
                    jobInfo['job_salary'] = ''

                # Get company logo Link
                job_company_logo_link = job.css("div.jobcard_logo").css("img::attr(src)")
                if(job_company_logo_link):
                    jobInfo['job_company_logo_link'] = job_company_logo_link.get().strip()
                else:
                    jobInfo['job_company_logo_link'] = ''

                # Job type (Full Time/Part Time/Contract)
                jobInfo['job_type'] = ''

                # Get link to the job and create a jobid for it
                job_description_link = job.css("h2").css("a::attr(href)")
                if(job_description_link):
                    jobInfo['job_description_link'] = 'https://www.indeed.co.in' + job_description_link[0].get()
                    jobInfo['job_id'] = hashlib.sha224(jobInfo['job_description_link'].encode('UTF-8')).hexdigest()  # Calculate job ID for Internal storage purpose (Shall be always same if 'job_description_link' is same)
                else:
                    jobInfo['job_description_link'] = ''
                    jobInfo['job_id'] = ''

                jobInfo["job_page_index"] = IndeedJobs.page_index

                if(jobInfo['job_description_link']):
                    request = scrapy.Request(jobInfo['job_description_link'], callback=self.parse_job_details, cb_kwargs=jobInfo)
                    yield request
                else:
                    yield 'NO_INFO'
            except Exception as err:
                print(err)

        next_page = f'https://www.indeed.co.in/jobs?q=elixir&l=India&start={IndeedJobs.page_index * 10}'

        print('########################--1')
        # print(response.css("div.pagination").css("li"))
        has_pagination_loaded = len(response.css("div.pagination").css("li"))>0
        # print(len(response.css("div.pagination").css("li")))
        is_last_index_inactive = has_pagination_loaded and len(response.css("div.pagination").css("li")[-1].css("b::attr(aria-label)"))==0
        # print(is_last_index_inactive)
        # print('########################--2')

        if is_last_index_inactive:  # Till the last page
            IndeedJobs.page_index += 1
            IndeedJobs.force_load_count = 0
            yield response.follow(next_page, callback=self.parse)
        elif ((not is_last_index_inactive) and (not has_pagination_loaded)): #Sometimes the pagination part does not get loaded, so using retry logic we can confirm if it has reached the end of the pagination or not
            if(IndeedJobs.force_load_count == 0):
                IndeedJobs.page_index += 1
                IndeedJobs.force_load_count += 1
                yield response.follow(next_page, callback=self.parse)
            elif(IndeedJobs.force_load_count > 0 and IndeedJobs.force_load_count < 3):
                IndeedJobs.force_load_count += 1
                yield response.follow(next_page, callback=self.parse)
            elif(IndeedJobs.force_load_count >= 3):
                IndeedJobs.force_load_count = 0

    def parse_job_details(self, response, **jobInfo):
        jobInfo['job_description_link'] = response.url
        if(response.css("div.jobsearch-jobDescriptionText")):
            jobInfo['job_description'] = html2text.html2text(response.css("div.jobsearch-jobDescriptionText").get())

        yield jobInfo
