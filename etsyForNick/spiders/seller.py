import scrapy


class SellerSpider(scrapy.Spider):
    name = 'seller'
    
    def start_requests(self):
        with open('links.csv') as f:
            for line in f:
                if not line.strip():
                    continue
                yield scrapy.Request(line, callback=self.parse)

    def parse(self, response):
        F_Name = response.xpath('//div[@class="img-container"]/a/@title').get()
        if F_Name:
            F_Name = F_Name.split(' ')[0]
        L_Name = response.xpath('//div[@class="img-container"]/a/@title').get()
        if L_Name:
            L_Name = L_Name.split(' ')[-1]
            
        NoofSales = response.xpath('//div[@class="shop-info"]//*[contains(text(), "Sales")]/text()').get()
        product = response.xpath('//button[@aria-selected="true"]/span[contains(text(), "All")]/following-sibling::span/text()').get()
        Admirers = response.xpath('//a[contains(text(), "Admirers")]/text()').get()
        shopLocation = response.xpath('//span[contains(@class, "shop-location")]/text()').get()
        country = response.xpath('//span[@data-in-modal-editable-text="user_location"]/text()').get()
        if country:
            country = country.split(',')[-1]
        custom = response.xpath('//span[contains(text(), "Sort: Custom")]/text()').get()
        if custom:
            custom = 'Y'
        else:
            custom = 'N'
        starSeller = response.xpath('(//p[contains(text(), "Star Seller")])[1]/text()').get()
        if starSeller:
            starSeller = 'Y'
        else:
            starSeller = 'N'
        starRating = response.xpath('//input[@name="rating"]/following-sibling::span[@class="wt-screen-reader-only"]/text()').get()
        blurbText = response.xpath('//div[contains(@class, "wt-show-xl wt-show-tv")]/p/span/text()').getall()
        blurbText = [item.strip() for item in blurbText]
        
        yield {
            'Store Name': response.url,
            'First Name of Seller': F_Name,
            'Last Name of Seller': L_Name,
            'No. of Sales': NoofSales,
            'No. of Products': product,
            'No. of Admirers': Admirers,
            'Location of Seller': shopLocation,
            'Country of Seller': country,
            'Request Custom Order (Y/N)': custom,
            'Star Seller (Y/N)': starSeller,
            'Rating (Stars)': starRating,
            "Raw 'blurb at top of storefront'": blurbText,
            'Urls': response.url
        }
