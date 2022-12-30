import scrapy
class aqarSpider(scrapy.Spider):
    name = 'aqarProperties'
    allowed_domains = ['aqarmap.com.eg']
    start_urls = ['https://aqarmap.com.eg/en/for-sale/apartment/cairo/']

    def parse(self, response):
        properties = response.css("div.search-Result-Card")
        for p in properties:
            property_page_url= 'https://aqarmap.com.eg'+p.xpath('//div[has-class("card-details-container")]/a/@href').get()
            yield scrapy.Request(url=property_page_url, callback=self.parse_detailsPage)

        nxtpage = response.css('#te-next-search-result-page').attrib['href']
        if nxtpage is not None:
            yield response.follow(nxtpage, callback=self.parse)
    def parse_detailsPage(self, response):
        property_response = response.xpath('//section[has-class("listing-details")]')
        try:
            yield {
                'address': property_response.css('a.text-inherit::text').get().replace('\n', ''),
                'type': property_response.xpath('//label[has-class("attributes")]//a[has-class("text-inherit")]//text()').get().replace('\n',''),
                'rooms': property_response.xpath('//label//span[@itemprop = "numberOfRooms"]//text()').get(),
                'bathrooms': property_response.xpath('//label[3]//span[@itemprop = "numberOfRooms"]//text()').get(),
                'area': property_response.xpath('//label[@itemprop = "floorSize"]//text()[2]').get().replace('\n', ''),
                'floor': property_response.xpath('//table[@class="listing-info table-info"]/tbody/tr[1]/td[2]/text()').get(),
                'year_built': property_response.xpath('//table[@class="listing-info table-info"]/tbody/tr[2]/td[2]/text()').get(),
                'finishing': property_response.xpath('//table[@class="listing-info table-info"]/tbody/tr[3]/td[2]/text()').get(),
                'view': property_response.xpath('//table[@class="listing-info table-info"]/tbody/tr[4]/td[2]/text()').get(),
                'price': property_response.xpath('//div[has-class("listing-price-content")]/span[has-class("integer")]/text()').get().replace('\xa0', ''),
            }
        except:
            yield {
                'address': '',
                'type': '',
                'rooms': '',
                'bathrooms':  '',
                'area': '',
                'floor': '',
                'year_built': '',
                'finishing': '',
                'view': '',
                'price': '',
            }


