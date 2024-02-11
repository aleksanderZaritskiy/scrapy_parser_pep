# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from collections import defaultdict

from .constants import BASE_DIR, FILE_NAME, DIR_RESULTS


class PepParsePipeline:
    count_status = defaultdict(int)

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.__class__.count_status[item['status']] += 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / DIR_RESULTS
        results_dir.mkdir(exist_ok=True)
        file_path = results_dir / FILE_NAME
        with open(file_path, mode='w', encoding='utf-8') as f:
            f.write('Status,Count\n')
            writer = csv.writer(
                f, dialect='unix', quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            writer.writerows(self.__class__.count_status.items())
            f.write(f'Total,{sum(self.__class__.count_status.values())}\n')
