import scrapy

class LispiderSpider(scrapy.Spider):
    name = "lispider"

    scraper_api_url = 'http://api.scraperapi.com'
    api_key = '9d48909da2144bc72f125ac753ef5da4'

    company_pages = [
        'https://www.linkedin.com/company/usebraintrust?trk=public_jobs_jserp-result_job-search-card-subtitle',
        'https://www.linkedin.com/company/techy-staffing/?trk=public_jobs_topcard-org-name&originalSubdomain=in',
        'https://www.linkedin.com/company/synergisticit/?trk=public_jobs_topcard-org-name',
        'https://www.linkedin.com/company/mindpal.co/?trk=public_jobs_topcard-org-name',
        'https://www.linkedin.com/company/steneral-consulting/?trk=public_jobs_topcard-org-name',
        'https://www.linkedin.com/company/lorventech/?trk=public_jobs_topcard-org-name',
        'https://www.linkedin.com/company/adameservices/?trk=public_jobs_topcard-org-name',
        'https://www.linkedin.com/company/medreviewinc/?trk=public_jobs_topcard-org-name',
        'https://www.linkedin.com/company/gersh-academy/?trk=public_jobs_topcard-org-name',
        'https://www.linkedin.com/company/hireblox/?trk=public_jobs_topcard-org-name',
        'https://www.linkedin.com/company/foxbox-digital/?trk=public_jobs_topcard-org-name',
        'https://www.linkedin.com/company/zealogics-inc/?trk=public_jobs_topcard-org-name',
        'https://www.linkedin.com/company/get-it-recruit-information-technology/?trk=public_jobs_topcard-org-name',
        'https://www.linkedin.com/company/center-for-justice-innovation/?trk=public_jobs_topcard-org-name',
        ]

    def start_requests(self):
        company_index_tracker = 0
        first_url = self.company_pages[company_index_tracker]
        url = f"{self.scraper_api_url}?api_key={self.api_key}&url={first_url}"

        yield scrapy.Request(
            url=url,
            callback=self.parse_response,
            meta={'company_index_tracker': company_index_tracker},
        )

    def parse_response(self, response):
        company_index_tracker = response.meta['company_index_tracker']
        self.logger.info(f'Scraping page {company_index_tracker+1} of {len(self.company_pages)}')

        company_item = {}
        company_item['name'] = response.css('.top-card-layout__entity-info h1::text').get(default='not-found').strip()
        company_item['summary'] = response.css('.top-card-layout__entity-info h4 span::text').get(default='not-found').strip()

        try:
            company_details = response.css('.core-section-container__content .mb-2')
            company_website_line = company_details[0].css('.text-md a::text').get()
            company_item['website'] = company_website_line.strip()
            company_industry_line = company_details[1].css('.text-md::text').getall()
            company_item['industry'] = company_industry_line[1].strip()
            company_size_line = company_details[2].css('.text-md::text').getall()
            company_item['size'] = company_size_line[1].strip()
            company_size_line = company_details[5].css('.text-md::text').getall()
            company_item['founded'] = company_size_line[1].strip()
        except IndexError:
            self.logger.error("Error: Skipped Company - Some details missing")

        yield company_item

        company_index_tracker = company_index_tracker + 1
        if company_index_tracker <= (len(self.company_pages) - 1):
            next_url = self.company_pages[company_index_tracker]

            yield scrapy.Request(
                url=next_url,
                callback=self.parse_response,
                meta={'company_index_tracker': company_index_tracker},
            )

        