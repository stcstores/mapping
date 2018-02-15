from mapping import CHANNELS, PRODUCTS


def test_products():
    assert len(PRODUCTS) > 0


def test_channels():
    assert [c.name for c in CHANNELS] == ['eBay UK', 'Amazon UK']


def test_get_link_url():
    assert PRODUCTS[0].links[0].url() == 'http://ebay.co.uk/itm/270961777649'
