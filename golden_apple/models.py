import json

from pydantic import BaseModel, field_validator, Field
from typing import List, Any


class ProductDetail(BaseModel):
    itemId: str | None

class ProductList(BaseModel):
    count: int
    products: List[ProductDetail]

    @field_validator('products') #приводит показатель к нужному значению, можно менять типы данных
    def set_products(cls, value):
        return [i.itemId for i in value]



class Description(BaseModel):
    text: str
    content: str

class Actual(BaseModel):
    amount: int
class Price(BaseModel):
    actual: Actual
class Variant(BaseModel):
    itemId: str
    price: Price

    @field_validator('price')
    def set_price(cls, value: Price):
        return value.actual.amount

class ProductData(BaseModel):
    id: str
    name: str
    brand: str
    productType: str
    productDescription: List[Description]
    variants: List[Variant]

    price: int = Field(default=0)
    description: str = Field(default='')
    application: str = Field(default='')
    composition: str = Field(default='')
    about_brand: str = Field(default='')
    addit_info: str = Field(default='')

    def model_post_init(self, __context: Any) -> None:
        self.price = int(next((i.price for i in self.variants if i.itemId == self.id), 0))

        attributes_map = {
            'описание': 'description',
            'применение': 'application',
            'состав': 'composition',
            'о бренде': 'about_brand',
            'Дополнительная информация': 'addit_info'
        }

        for desc in self.productDescription:
            attributes_name = attributes_map.get(desc.text)
            if attributes_name:
                setattr(self, attributes_name, desc.content)

        #     if desc.text == 'описание':
        #         self.description = desc.content
        #     elif desc.text == 'применение':
        #         self.application = desc.content
        #     elif desc.text == 'состав':
        #         self.composition = desc.content
        #     elif desc.text == 'о бренде':
        #         self.about_brand = desc.content
        #     elif desc.text == 'Дополнительная информация':
        #         self.addit_info = desc.content

        del self.__dict__['productDescription']
        del self.__dict__['variants']

    def to_tuple(self) -> tuple:
        return tuple(self.__dict__.values())



# with open('test.json', encoding='utf-8') as f:
#     data = json.load(f)
#
# pd_data = ProductData(**data)
# for i in pd_data:
#     print(i)