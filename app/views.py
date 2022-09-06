from app import app
from flask import render_template
from .request import get_news_source, publishedArticles, randomArticles, topHeadlines, get_article, generate_article_templates, get_tags, get_article_from_db


@app.route('/')
def home():
    articles = publishedArticles()
    sources = get_news_source()
    tags = get_tags()

    title = " All Articles"
    return render_template('home.html', articles=articles, title=title, sources=sources, tags=tags)


@app.route('/headlines')
def headlines():
    headlines = topHeadlines()

    return render_template('headlines.html', headlines=headlines)


@app.route('/articles')
def articles():
    random = randomArticles()

    return render_template('articles.html', random=random)


@app.route('/sources')
def sources():
    newsSource = get_news_source()


    return render_template('sources.html', newsSource=newsSource)


@app.route('/tags/<tag>')
def articles_by_filter_tag(tag):

    articles = generate_article_templates(1000, tag=tag)
    sources = get_news_source()
    tags = get_tags()

    title = f"Filtered by Tag: {tag}"
    return render_template('home.html', articles=articles, title=title, sources=sources, tags=tags)


@app.route('/article/<article_id>')
def article(article_id):

    print('yoooooooo')
    article = get_article_from_db(article_id)


    return render_template('article.html', article=article)
