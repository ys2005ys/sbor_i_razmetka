import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import UplushImgItem
from itemloaders.processors import MapCompose


class SpiderImgSpider(CrawlSpider):
    name = "spider_img"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com/images/sports/baseball"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//a[@class='Prxeh']")), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths=("//div[@class='UYsLB VfiJa ec_09 Niw9H _UNLg']/button[@type='button']")))
    )

    def parse_item(self, response):
        loader = ItemLoader(item=UplushImgItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)

        loader.add_xpath("author_image", "//div[@class='TeuLI']/a/text()")

        loader.add_xpath('Published', '//time/text()')

        categories = response.xpath('//div[@class="zDHt2 N9mmz"]/a/text()').getall()
        loader.add_value('categories', categories)

        description = response.xpath("//div[@class='WxXog']/img/@alt").get()
        loader.add_value('description', description)

        image_url = response.xpath("//div[@class='WxXog']/img/@src").get()
        loader.add_value('image_urls', image_url)

        yield loader.load_item()
