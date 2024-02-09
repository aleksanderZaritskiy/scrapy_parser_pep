import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        peps = response.xpath("id('numerical-index')//tbody//tr")

        for pep in peps:
            link = pep.xpath("td/following-sibling::td/a/@href").get()
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css("#pep-content .page-title::text").get()
        number, name = 0, ''
        for index in range(len(title)):
            char = title[index]
            if char.isdigit():
                number = number * 10 + int(char)
            elif char == '–':
                name = title[index + 2:]
                break

        status = response.xpath(
            ("id('pep-content')//dl/dt[contains(., 'Status')]"
             "/following-sibling::dd/abbr/text()")
        ).get()

        data = {
            'number': number,
            'name': name,
            'status': status,
        }
        yield PepParseItem(data)
