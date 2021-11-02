# -*- coding: utf-8 -*-
import scrapy
from data_checker.items import Dataset


class DatasetSpider(scrapy.Spider):
    name = "dataset"
    allowed_domains = ["catalog.data.gov"]
    start_urls = ["https://catalog.data.gov/dataset"]

    def parse(self, response):
        host = response.url.split("/dataset")[0]
        for dataset in response.css(".dataset-content"):
            yield Dataset(
                name=dataset.css("h3.dataset-heading > a::text").get(),
                link=host + dataset.css("h3.dataset-heading >a::attr(href)").get(),
                organization=dataset.css(".dataset-organization::text")
                .get()
                .strip(" —"),
            )
