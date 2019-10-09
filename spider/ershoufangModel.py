from peewee import *

database = MySQLDatabase('secondhand', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '127.0.0.1','port':53306,'user': 'root', 'password': '123456'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Chengjiao(BaseModel):
    area = CharField(null=True)
    floor = CharField(null=True)
    price = IntegerField(null=True)
    room_info = CharField(null=True)
    sale_price = IntegerField()
    sale_time = DateTimeField(null=True)
    time = IntegerField(null=True)
    xiaoqu_name = CharField(null=True)

    class Meta:
        table_name = 'chengjiao'

class Ershoufang(BaseModel):
    area = CharField(null=True)
    area_in = CharField(null=True)
    elevator = CharField(null=True)
    location = CharField(null=True)
    price = IntegerField()
    room_maininfo = CharField(null=True)
    room_subinfo = CharField(null=True)
    room_type = CharField(null=True)
    sale_time = CharField(null=True)
    unit_price = IntegerField(null=True)
    xiaoqu_name = CharField()

    class Meta:
        table_name = 'ershoufang'

class Xiaoqu(BaseModel):
    address = CharField(null=True)
    building = CharField(null=True)
    city = CharField(null=True)
    city_code = IntegerField(column_name='cityCode', null=True)
    company = CharField(null=True)
    name = CharField(null=True)
    number = CharField(null=True)
    price = IntegerField(null=True)
    property_company = CharField(null=True)
    property_fee = CharField(null=True)
    source = CharField(null=True)
    type = CharField(null=True)

    class Meta:
        table_name = 'xiaoqu'


if __name__ == "__main__":
    Xiaoqu.create_table()
    Chengjiao.create_table()
    Ershoufang.create_table()