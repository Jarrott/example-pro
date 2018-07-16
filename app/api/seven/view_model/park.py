# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/07/16 
"""
import time


class ParkCollection:
    def __init__(self, park_list):
        self.data = []
        for park in park_list:
            self.data.append(ParkNewsViewModel(park))


class ParkNewsViewModel:
    def __init__(self, park):
        self.title = park.title
        self.create_time = time.strftime('%Y-%m-%d')
        self.image = park.image
        self.content = park.content

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return ['title', 'create_time', 'image', 'content']
