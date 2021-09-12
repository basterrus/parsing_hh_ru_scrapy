import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def link_join(value):
    try:
        link = ''.join(value)
    except:
        pass
    return value


def images_replace(value):
    try:
        value = value.replace('w_82,h_82,', '')
    except:
        pass
    return value


def text_replace(value):
    try:
        value = value.replace('\n', '')
    except:
        pass
    return value


def price_replace(value):
    new_value = []
    for i in value:
        if i.isdigit():
            new_value.append(i)
    try:
        return int(''.join(new_value))
    except:
        return value


class LmruItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(price_replace), output_processor=TakeFirst())
    link = scrapy.Field(input_processor=MapCompose(link_join), output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    # spec = scrapy.Field(input_processor=MapCompose(text_replace), output_processor=TakeFirst())
    images = scrapy.Field(input_processor=MapCompose(images_replace), output_processor=TakeFirst())

    # characteristic_key = scrapy.Field()
    # characteristic_value = scrapy.Field()
