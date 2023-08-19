import scrapy


class LispiderSpider(scrapy.Spider):
    name = "lispider"
    allowed_domains = ["www.linkedin.com"]
    start_urls = ["https://www.linkedin.com/jobs/search"]

    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=python&location=%D0%A1%D0%BE%D0%B5%D0%B4%D0%B8%D0%BD%D0%B5%D0%BD%D0%BD%D1%8B%D0%B5%20%D0%A8%D1%82%D0%B0%D1%82%D1%8B%20%D0%90%D0%BC%D0%B5%D1%80%D0%B8%D0%BA%D0%B8&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start='

    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})

    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        job_item = {}
        print(job_item)
        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        print("******* Num Jobs Returned *******")
        print(num_jobs_returned)
        print('*****')

        for job in jobs:
            
            job_item['job_title'] = job.css("h3::text").get(default='not-found').strip()
            job_item['job_detail_url'] = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
            job_item['job_listed'] = job.css('time::text').get(default='not-found').strip()

            job_item['company_name'] = job.css('h4 a::text').get(default='not-found').strip()
            job_item['company_link'] = job.css('h4 a::attr(href)').get(default='not-found')
            job_item['company_location'] = job.css('.job-search-card__location::text').get(default='not-found').strip()
            yield job_item

        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + 25
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})