import json
import requests
from bs4 import BeautifulSoup

from .models import Post


def aggregate(url, tag, tag_class):
    site = requests.get(url)
    soup = BeautifulSoup(site.text, 'lxml')
    posts = soup.find_all(tag, class_=tag_class)
    
    for news in posts:
        source = news.a['href']
        title = news.text
        image = news.find('img')
        
        news = Post.objects.create(source=source, title=title, content=title, image=image)
        news.save()


if __name__ == "__main__":
    with open('./sites.json', 'r') as file:
        sites = json.load(file)

        for _link, _tag, _class in sites.values():
            aggregate(_link, _tag, _class)
