# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/07/16 
"""
from app.libs.helper import str_timestamp


class ParkCollection:
    def __init__(self, park_list):
        self.data = []
        for park in park_list:
            self.data.append(ParkNewsViewModel(park))


class ParkNewsViewModel:
    def __init__(self, park):
        self.title = park.title
        self.create_time = str_timestamp(park.create_time)
        self.image = park.image
        self.content = park.content

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return ['title', 'create_time', 'image', 'content']
