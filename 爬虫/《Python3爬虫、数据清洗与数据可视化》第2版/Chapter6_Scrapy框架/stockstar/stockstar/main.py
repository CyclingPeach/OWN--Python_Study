from scrapy.cmdline import execute

# 将爬取的数据导入到items.json文件中
# scrapy crawl stock -o items.json
execute(["scrapy", "crawl", "stock", "-o", "items.json"])