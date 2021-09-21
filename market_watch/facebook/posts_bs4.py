#!/usr/bin/python

import requests
from bs4 import BeautifulSoup


class FBGroupScraper:

    def __init__(self, group_id):
        self.group_id = group_id
        self.page_url = "https://mobile.facebook.com/%s/" % self.group_id
        self.page_content = ""

    def get_page_content(self):
        print(self.page_url)
        self.page_content = requests.get(self.page_url).text

    def parse(self):
        soup = BeautifulSoup(self.page_content, "html.parser")
        #print("soup: %s" % soup)
        feed_container = soup.find(id="m_group_stories_container").find_all("p")
        for i in feed_container:
            print(i.text)

group_id = "shensimon"
d = FBGroupScraper(group_id)
d.get_page_content()
d.parse()

