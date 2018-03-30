import facebook
import os
import json
import urllib
import pprint

ACCESS_TOKEN = "EAACEdEose0cBAF3L5xQfGmbBfGjHW3u51iyM53ZCev7LLZBEfozwgpvoKpdKF9GZCKa27X8EZC8cJYKhzkbFnCm9sGmpFrZC4fAZBVV6eJDDqbkQnEUUWkDfhehD4fRLqjhOBwR7ZBCvpgvBqO3qUghSAIYfjguI47TWeNUJ0P0I3EMxisBYsSEg5AXC94zxaPQWmXQpIjrZAAZDZD"
graph = facebook.GraphAPI(ACCESS_TOKEN)

# For now using dummy companies/fields to show how it works
company = "820882001277849"  # Coca-Cola
fields = ['id', 'name', 'posts']

request = company + "?fields="

for field in fields:
    request = request + field + ","

request = request[:-1]

post = graph.request(request)
print(post)
