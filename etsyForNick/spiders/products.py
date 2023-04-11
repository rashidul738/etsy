import scrapy


f = [
    'https://www.etsy.com/listing/955609172/pallet-blank-plain-coir-doormats-craft',
    'https://www.etsy.com/listing/1229701511/please-use-the-spray-bathroom-doormat',
    'https://www.etsy.com/listing/1229728289/please-flush-toilet-bathroom-doormat',
    'https://www.etsy.com/listing/1229731087/please-remain-seated-bathroom-doormat',
    'https://www.etsy.com/listing/1229745291/soak-your-troubles-bathroom-doormat',
    'https://www.etsy.com/listing/1215799926/poops-about-to-go-down-bathroom-doormat',
    'https://www.etsy.com/listing/1215872954/wipe-it-real-good-bathroom-doormat',
]

class ProductsSpider(scrapy.Spider):
    name = 'products'
    def start_requests(self):
        # with open('links.csv') as f:
        for line in f:
            if not line.strip():
                continue
            yield scrapy.Request(line, callback=self.parse_details)

    # def parse(self, response):
    #     links = response.xpath('//div[contains(@class, "responsive-listing-grid")]//a/@href').extract()
    #     for link in links:
    #         yield scrapy.Request(link, callback=self.parse_details, meta={'urls_1': response.url})
            
    #     next_page = response.xpath('(//a[@class="wt-action-group__item wt-btn wt-btn--icon "])[4]/@href').get()
    #     if next_page:
    #         yield scrapy.Request(next_page, callback=self.parse)
        
        
    def parse_details(self, response):
        shopName = response.xpath('//a[contains(@aria-label, "View more products from store owner")]/span/text()').get()
        if shopName:
            shopName = shopName.strip()
            
        p_url = response.xpath('//a[contains(@aria-label, "View more products from store owner")]/@href').get()
        
        product_name = response.xpath('//div[@class="wt-mb-xs-2"]/h1/text()').get()
        if product_name is not None:
            product_name = product_name.strip()
            
        rowDetails = response.xpath('//div[@id="product-details-content-toggle"]//li/div/text()|//div[@id="product-details-content-toggle"]//p/text()').getall()
        rowDetails = [item.strip() for item in rowDetails]
        
        rowProductDescription = response.xpath('//div[@id="wt-content-toggle-product-details-read-more"]/p/text()|//div[@id="wt-content-toggle-product-details-read-more"]/p/a/@href').getall()
        rowProductDescription = [item.strip() for item in rowProductDescription]
        
        review = response.xpath('//h2[contains(text(), "reviews")]/text()').get()
        if review:
            review = review.strip()
        else:
            review = "0"
            
        productPrice = response.xpath('//span[contains(text(), "Price:")]/following-sibling::text()').get()
        if productPrice is not None:
            productPrice = productPrice.strip()
            
        customaizationTitle = response.xpath('//label[contains(@for, "variation-selector")]/text()').getall()
        customaizationTitle = [item.strip() for item in customaizationTitle]
            
        
        yield {
            'Seller Name': shopName,
            'Seller URL': p_url,
            'Product Name': product_name,
            'Details Text': rowDetails,
            'Description Text': rowProductDescription,
            'Number of Reviews for this Item': review,
            'Price': productPrice,
            'Customization Titles': customaizationTitle,
            'Url': response.url
        }
        

