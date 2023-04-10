import scrapy


class ScnSpider(scrapy.Spider):
    name = 'SCN'
    
    def start_requests(self):
        with open('links.csv') as f:
            for line in f:
                if not line.strip():
                    continue
                yield scrapy.Request(line, callback=self.parse)

    def parse(self, response):
        sellerName = response.xpath('//div[contains(@class, "shop-name-and-title")]/h1/text()').get()
        for product in response.xpath('//ul[@class="wt-tab wt-flex-direction-column-md wt-bb-xs-none vertical-tabs"]/button'):
            # seller = sellerName
            # catagorname = product.xpath('.//span[1]/text()').get().strip()
            catagorname = product.xpath('./span[1]/text()|./span[1]/span[1]/text()').getall()
            if catagorname:
                catagorname = [item.strip() for item in catagorname]
            quantity = product.xpath('./span[2]/text()').get()
            # urls = product.xpath('.//@data-section-id').get()
            # url = response.url + "?section_id=" + urls
            
            yield {
                'Seller namec': sellerName,
                'Category': catagorname,
                'Number of Items': quantity,
                'URL': response.url
                
            }
