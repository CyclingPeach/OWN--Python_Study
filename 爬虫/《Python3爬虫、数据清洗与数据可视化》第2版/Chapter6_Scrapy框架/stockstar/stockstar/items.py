import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst


class StockstarItemLoader(ItemLoader):
    #自定义itemloader, 用户存储爬虫所抓取的字段内容
    default_output_processor = TakeFirst()


class StockstarItem(scrapy.Item):
    # define the fields(字段) for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()       # 股票代码
    abbr = scrapy.Field()       # 简称
    circulation_market_Value  = scrapy.Field()      # 流通市值
    total_Market_Value        = scrapy.Field()      # 总市值
    circulation_capital       = scrapy.Field()      # 流通股本
    total_capital             = scrapy.Field()      # 总股本
