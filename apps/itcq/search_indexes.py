from haystack import site
from cms.models import Page
from haystack import indexes


class PageIndex(indexes.SearchIndex):
    title = indexes.CharField(model_attr="get_page_title")
    description = indexes.CharField(model_attr="get_meta_description")
    keywords = indexes.CharField(model_attr="get_meta_keywords")
    text = indexes.CharField(document=True, use_template=True)

site.register(Page, PageIndex)
