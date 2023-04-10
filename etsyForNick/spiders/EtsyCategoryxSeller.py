import scrapy


class EtsycategoryxsellerSpider(scrapy.Spider):
    name = 'EtsyCategoryxSeller'
    allowed_domains = ['etsy.com']
    start_urls = ['http://etsy.com/']

    def parse(self, response):
        sellerName = response.xpath('//div[contains(@class, "shop-name-and-title")]/h1/text()').get()
        for product in response.xpath('//ul[@class="wt-tab wt-flex-direction-column-md wt-bb-xs-none vertical-tabs"]/button'):
            # seller = sellerName
            # catagorname = product.xpath('.//span[1]/text()').get().strip()
            catagorname = product.xpath('./span[@class="wt-break-word wt-mr-xs-2"]/span[1]/text()').get()
            quantity = product.xpath('./span[2]/text()').get()
            urls = product.xpath('.//@data-section-id').get()
            url = response.url + "?section_id=" + urls
            
            yield {
                'Seller namec': sellerName,
                'Category': catagorname,
                'Number of Items': quantity,
                'URL': url,
            }
