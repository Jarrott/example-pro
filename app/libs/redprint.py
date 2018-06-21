# -*- encoding:utf-8 -*-
"""
@ Created by Seven on  2018/06/20 
"""


class Redprint:
    """
    根据蓝图实现宏图
    """

    def __init__(self, name, with_prefix=True):
        self.name = name
        self.with_prefix = with_prefix
        self.mound = []

    def route(self, rule, **options):
        """重构蓝图的路由
        """

        def decorator(f):
            self.mound.append((f, rule, options))
            return f

        return decorator

    def register(self, app, url_prefix=None):
        """
        重构蓝图中的register函数
        """
        if url_prefix is None and self.with_prefix:
            url_prefix = '/' + self.name
        else:
            url_prefix = ''

        for f, rule, options in self.mound:
            endpoint = self.name + '+' + \
                       options.pop("endpoint", f.__name__)

            if rule:
                url = url_prefix + rule
                app.add_url_rule(url, endpoint, f, **options)
            else:
                app.add_url_rule(url_prefix, endpoint, f, **options)
