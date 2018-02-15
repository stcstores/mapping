import os

from jinja2 import Template

from .channels import CHANNELS as channels
from .productrange import PRODUCT_RANGES as ranges
from .products import PRODUCTS as products


class Main:

    def __init__(self, output_path):
        template_path = os.path.join(
            os.path.dirname(__file__), 'template.html')

        with open(template_path, 'r') as template_file:
            template = Template(template_file.read())
        context = {
            'products': products, 'channels': channels, 'ranges': ranges}
        output = template.render(context)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
