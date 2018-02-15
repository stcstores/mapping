import os

from tabler import Table

from . import paths
from .channels import CHANNELS
from .productrange import PRODUCT_RANGES


class Product:

    def __init__(self, row):
        self.sku = row['VAR_SKU']
        self.range_sku = row['RNG_SKU']
        if self.range_sku in PRODUCT_RANGES.keys():
            self.product_range = PRODUCT_RANGES[self.range_sku]
        else:
            self.product_range = PRODUCT_RANGES.add_range(row)
        self.stock_level = int(row['VAR_Stock'])
        self.title = row['VAR_Name']
        self.department = row['OPT_Department_MST']
        self.links = self.get_links()
        self.channel_links = {}
        for link in self.links:
            link.product = self
            link.product_range = self.product_range
            if link.channel not in self.channel_links:
                self.channel_links[link.channel] = []
            self.channel_links[link.channel].append(link)
        self.product_range.add_product(self)

    @property
    def linked(self):
        return any([len(self.links[channel]) > 0 for channel in self.links])

    @property
    def search_terms(self):
        search_terms = [self.sku, self.range_sku, self.title]
        for link in self.links:
            search_terms += link.search_terms
        return search_terms

    def get_links(self):
        links = []
        for channel in CHANNELS:
            if self.sku in channel.linking:
                links += channel.linking[self.sku]
        return links


class Products:
    def __init__(self):
        inventory_path = os.path.join(paths.FILES, 'ProductsExport.xlsx')
        self.inventory = Table(inventory_path)
        self.products = [Product(row) for row in self.inventory]
        self.departments = list(set([p.department for p in self.products]))

    def __iter__(self):
        for product in self.products:
            yield product

    def __getitem__(self, index):
        return self.products[index]

    def __len__(self):
        return len(self.products)


PRODUCTS = Products()
