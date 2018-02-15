import json


class ProductRange:

    def __init__(self, row):
        self.sku = row['RNG_SKU']
        self.title = row['RNG_Name']
        self.department = row['OPT_Department_MST']
        self.products = []
        self.links = []
        self.channel_links = {}

    def __repr__(self):
        return '{} - {}'.format(self.sku, self.title)

    def __iter__(self):
        for product in self.products:
            yield product

    def __getitem__(self, index):
        return self.products[index]

    def __len__(self):
        return len(self.products)

    def add_product(self, product):
        self.products.append(product)
        self.links += product.links
        for channel, links in product.channel_links.items():
            if channel not in self.channel_links:
                self.channel_links[channel] = []
            self.channel_links[channel] += links

    @property
    def stock_level(self):
        return sum([p.stock_level for p in self.products])

    @property
    def search_terms(self):
        search_terms = [self.sku, self.title]
        for product in self.products:
            search_terms += product.search_terms
        return search_terms

    def to_dict(self):
        return {
            str(channel.id): [link.to_dict() for link in links]
            for channel, links in self.channel_links.items()}

    def to_json(self):
        return json.dumps(self.to_dict())


class ProductRanges:

    def __init__(self):
        self.ranges = {}

    def __iter__(self):
        for sku, product_range in self.ranges.items():
            yield product_range

    def __getitem__(self, index):
        return self.ranges[index]

    def __len__(self):
        return len(self.ranges)

    def keys(self):
        return self.ranges.keys()

    def items(self):
        return self.ranges.items()

    def add_range(self, row):
        product_range = ProductRange(row)
        self.ranges[product_range.sku] = product_range
        return product_range

    def to_dict(self):
        return {r.sku: r.to_dict() for sku, r in self.ranges.items()}

    def to_json(self):
        return json.dumps(self.to_dict())


PRODUCT_RANGES = ProductRanges()
