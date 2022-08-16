from app import app
from flask import render_template
from .request import get_news_source, publishedArticles, randomArticles, topHeadlines, get_article


@app.route('/')
def home():
    articles = publishedArticles()

    return render_template('home.html', articles=articles)


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


@app.route('/category/<tag>')
def business(tag):
    sources = topHeadlines(tag)

    return render_template('category.html', sources=sources)


@app.route('/article/<article_id>')
def article(article_id):
    news_article = get_article(article_id)

    return render_template('article.html', article=news_article)
