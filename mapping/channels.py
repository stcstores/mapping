import json
import os
from uuid import uuid4

from tabler import Table

from . import paths


class Channel:

    def __init__(self, country, channel_id):
        self.id = uuid4()
        self.country = country
        self.channel_id = channel_id
        self.export_file = Table(self.path)
        self.linking = {}
        for row in self.export_file:
            sku = row['MapToSKU']
            if sku not in self.linking:
                self.linking[sku] = []
            self.linking[sku].append(self.link_class(self, row))

    def __repr__(self):
        return self.name

    @property
    def name(self):
        return '{} {}'.format(self.channel_name, self.country)

    @property
    def filename(self):
        return 'MappingExport_Mapped_{}.xlsx'.format(self.channel_id)

    @property
    def path(self):
        return os.path.join(paths.FILES, self.filename)


class Link:

    def __init__(self, channel, row):
        self.link_id = uuid4()
        self.channel = channel
        self.id = row['ItemID']
        self.product_sku = row['MapToSKU']
        self.channel_sku = row['SKU']
        self.title = row['Title']
        self.barcode = row['Barcode']
        self.url = self.get_url()

    def __repr__(self):
        return '{} linked to {} on {}'.format(
            self.product_sku, self.channel_sku, self.channel)

    @property
    def search_terms(self):
        return [
            self.link_id, self.channel_sku, self.product_sku, self.title,
            self.barcode]

    def to_dict(self):
        return {
            'channel': self.channel.name,
            'product_sku': self.product.sku,
            'product_title': self.product.title,
            'channel_sku': self.channel_sku,
            'channel_title': self.title,
            'channel_id': self.channel_id,
            'channel_id_name': self.channel_id_name,
            'domain': self.domain,
            'url': self.url}

    def to_json(self):
        json.dumps(self.to_dict())


class EBayLink(Link):

    domain = 'ebay.co.uk'
    channel_id_name = 'Listing ID'

    def __init__(self, channel, row):
        self.listing_id = row['ListingID']
        self.channel_id = self.listing_id
        super().__init__(channel, row)

    def get_url(self):
        return 'http://{}/itm/{}'.format(self.domain, self.listing_id)


class AmazonLink(Link):

    domain = 'amazon.co.uk'
    channel_id_name = 'ASIN'

    def __init__(self, channel, row):
        self.is_fba = row['IsFBA'] == 'True'
        self.asin = row['ASIN']
        self.channel_id = self.asin
        super().__init__(channel, row)

    def get_url(self):
        return 'http://{}/dp/{}'.format(self.domain, self.asin)


class EBay(Channel):
    channel_name = 'eBay'
    link_class = EBayLink


class Amazon(Channel):
    channel_name = 'Amazon'
    link_class = AmazonLink


class Channels:
    channels = [
        EBay('UK', '3572_461'),
        Amazon('UK', '2803_412'),
        Amazon('AU', '5315_605'),
        Amazon('JP', '5240_627'),
        Amazon('CA', '2809_413'),
        Amazon('FR', '2806_412'),
        Amazon('DE', '2804_412'),
    ]

    def __iter__(self):
        for channel in self.channels:
            yield channel

    def __getitem__(self, index):
        return self.channels[index]


CHANNELS = Channels()
