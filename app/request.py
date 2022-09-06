import json
import urllib.request
#from .models import Article, Tag, Article_Tag, Publisher, tag_arts, art_tags, create_test_data
from .models import Article, Tag, Publisher, create_test_data

from .config import Config

from app import db


api_key = None
base_url = None
base_url_for_everything = None
base_url_top_headlines = None
base_source_list = None


def article_to_json(article):

    ret_json = {'title': f'{article.title}',
                'author': f'{article.author}',
                'img': f'{article.img}',
                'p_date': f'{article.p_date}',
                'content': f'{article.content}',
                'pub_id': f'{article.pub_id}',
                'desc': f'{article.desc}',
                'source': f'{article.publisher.publisher}',
                'tag': f'{article.tag.tag}',
                'id': f'{article.id}',

                }
    print(article)

    return ret_json


def generate_article_templates(number, tag=None):

    ret_articles = []
    final_number = number
    rows = Article.query.count()
    if rows < number:
        final_number = rows

    all_articles = None
    if tag:
        all_articles = get_most_recent_articles(final_number, tag)
    else:
        all_articles = get_most_recent_articles(final_number)

    for art in all_articles:
        ret_articles.append(article_to_json(art))

    return ret_articles


def get_id_by_tag(tag):
    tag_i = Tag.query.filter_by(tag=tag).first()
    ret_tag = 0
    if tag_i:
        ret_tag = tag_i.id
    return ret_tag


def get_tag_by_id(id):
    tag = Tag.query.filter_by(id=id).first()
    print('TAG')
    print(tag)
    return int(tag.id)

def get_most_recent_articles(number, tag=None):
#    print('creating test data')
#    create_test_data()

#    article = Article.query.filter_by(id=article_id).first()
#    articles = db.select().order_by(Article.id.desc()).limit(5)
    articles = None

    if tag:
#        tag_a = get_tag_by_id(tag)
        tag_a = get_id_by_tag(tag)
#        articles = db.session.query(Article).filter(Article.tag == tag_a).all()
        articles = Article.query.filter(Article.tag_id == tag_a).order_by(Article.id.desc()).limit(number).all()
    else:
        articles = Article.query.order_by(Article.id.desc()).limit(number).all()
#    article = Article.query.filter_by(id=article_id).order_by(Article.id.desc()).limit(5)
    return articles


def get_article_from_db(article_id):
    print('in db')
    article = Article.query.filter_by(id=article_id).first()

    article = article_to_json(article)

    return article



def publishedArticles():
    all_articles = generate_article_templates(Config.MAX_ARTICLES)
    return all_articles


def topHeadlines(tag=None):
    # newsapi = NewsApiClient(api_key=Config.API_KEY)
    #
    # if tag:
    #     articles = newsapi.get_top_headlines(category=tag)
    # else:
    #     top_headlines = newsapi.get_top_headlines(
    #         sources='cnn, reuters, cnbc, techcrunch, the-verge, gizmodo, the-next-web, techradar, recode, ars-technica')
    #
    # all_articles = articles['articles']
    # return zip_content(all_headlines)

    if tag:
        all_headlines = generate_article_templates(Config.MAX_ARTICLES, tag)
    else:
        all_headlines = generate_article_templates(Config.MAX_ARTICLES)

    return zip_content(all_headlines)


def randomArticles():
    # newsapi = NewsApiClient(api_key=Config.API_KEY)
    #
    # random_articles = newsapi.get_everything(sources='the-verge, gizmodo, the-next-web, recode, ars-technica')
    #
    # all_articles = random_articles['articles']
    all_articles = generate_article_templates(Config.MAX_ARTICLES)

    return zip_content(all_articles)


def get_news_source():
    '''
    Function that gets the json response to our url request
    '''
    publishers = Publisher.query.all()
    pubs = []
    for pub in publishers:
        print(pub.publisher)
        pubs.append(pub.publisher)
    return pubs


def get_tags():
    '''
    Function that gets the json response to our url request
    '''
    tagss = Tag.query.all()
    tags = []
    for tag in tagss:
        print(tag.tag)
        tags.append(tag.tag)
    return tags

    """
    get_news_source_url = 'https://newsapi.org/v2/sources?apiKey=' + Config.API_KEY
    with urllib.request.urlopen(get_news_source_url) as url:
        get_news_source_data = url.read()
        get_news_source_response = json.loads(get_news_source_data)

        news_source_results = None

        if get_news_source_response['sources']:
            news_source_results_list = get_news_source_response['sources']
            news_source_results = process_sources(news_source_results_list)
"""
    return news_source_results


def process_sources(source_list):
    '''
    function that process the news articles and transform them to a list of objects
    '''
    news_source_result = []
    for news_source_item in source_list:
        name = news_source_item.get('name')
        description = news_source_item.get('description')
        url = news_source_item.get('url')
    return news_source_result


def get_article(article_id):
    return generate_article_templates(1, article_id)[0]
