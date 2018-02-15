from tabler import Table

from .channels import CHANNELS as channels
from .productrange import PRODUCT_RANGES as ranges


class Main:

    def __init__(self, output_path):

        header = ['Range SKU', 'Range Title', 'Stock Level', 'Search SKU']
        for channel in channels:
            header.append(channel.name)
        data = []

        for product_range in ranges:
            row = [
                product_range.sku, product_range.title,
                product_range.stock_level, product_range.products[0].sku]
            for channel in channels:
                if channel in product_range.channel_links:
                    row.append(len(product_range.channel_links[channel]))
                else:
                    row.append(0)
            data.append(row)
        Table(header=header, data=data).write(output_path)
