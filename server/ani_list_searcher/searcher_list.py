from ani_list_searcher.web_searcher.searcher_list import searcher_list as web_searcher_list
from functools import cache

@cache
def searcher_list():
    return web_searcher_list()

@cache
def searcher_dict():
    return {i.name: i for i in searcher_list()}