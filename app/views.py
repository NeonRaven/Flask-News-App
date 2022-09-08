from app import app
from flask import render_template, request, redirect, flash, abort, Response
from .request import get_news_source, publishedArticles, get_article, generate_article_templates, get_tags, get_article_from_db, get_source_name_from_source_id, allowed_file, get_tag_detailed, create_article
import os
from werkzeug.utils import secure_filename
from uuid import uuid4

import io
import json
import base64


@app.route('/')
def home():
    articles = publishedArticles()
    sources = get_news_source()
    tags = get_tags()

    for art in articles:
        print(art['title'])
        print(art['art_tags'])

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


@app.route('/sources/<source_id>')
def source(source_id):
    articles = generate_article_templates(1000, tag=None, source=source_id)
    sources = get_news_source()
    tags = get_tags()
    source_name = get_source_name_from_source_id(source_id)

    title = f"Filtered by Publisher Source: {source_name}"
    return render_template('home.html', articles=articles, title=title, sources=sources, tags=tags)


@app.route('/tags/<tag>')
def articles_by_filter_tag(tag):

    articles = generate_article_templates(1000, tag=tag)
    sources = get_news_source()
    tags = get_tags()

    title = f"Filtered by Tag: {tag}"
    return render_template('home.html', articles=articles, title=title, sources=sources, tags=tags)


@app.route('/article/<article_id>')
def article(article_id):

    article = get_article_from_db(article_id)

    return render_template('article.html', article=article)


@app.route('/success/')
def successful():
    print('success?')
    return render_template('post_success.html')

@app.route('/failure/')
def failure():
    print('failure?')
    return render_template('post_failure.html')



@app.route('/new/', methods=['GET'])
def new_story():
    sources = get_news_source()
    print('i am tags')
    tags = get_tag_detailed()
    print(tags)

    return render_template('home2.html', allowed_pubs=sources, tags=tags)

@app.route('/new_story/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        print('i am a post')
        print(request.form)
        print(request.files)

        if 'title' in request.form and 'desc' in request.form and 'author' in request.form and 'content' in request.form:
            if len(request.form['title'])>0 and len(request.form['desc'])>0 and len(request.form['author'])>0 and len(request.form['content'])>0:
                print(request.form['title'])
                print(len(request.form['title']))
                print(request.form['desc'])
                print(request.form['author'])
                print(request.form['content'])
                print(request.form['publisher'])

                tags = None
                if 'tags' in request.form:
                    tags = request.form.getlist('tags')



                # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No image')
#                    return redirect(request.url)
                    return redirect('/failure/')

                file = request.files['file']
                print('we have file')
                if file.filename == '':
                    flash('No selected image')
#                    return redirect(request.url)
                    return redirect('/failure/')

                if file and allowed_file(file.filename):
                    fn_prefix = str(uuid4())[-12:-1]
                    filename = secure_filename(fn_prefix + file.filename)
                    file_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
                    file.save(os.path.join(file_path, filename))

                    create_article(request.form['title'],
                                   request.form['desc'],
                                   request.form['author'],
                                   request.form['content'],
                                   os.path.join('/images/', filename),
                                   request.form['publisher'],
                                   tags=tags
                                   )

                    flash('Complete!')
                    return redirect('/success/')

            else:
                flash('Missing information from article')
#                return redirect(request.url)
                return redirect('/failure/')

        else:
            flash('Missing information from article')
#            return redirect(request.url)
            return redirect('/failure/')

        ret = '{"code":200, "data": "ok"}'
        resp = Response(response=ret,
                        status=200,
                        mimetype="application/json")
        return resp

    else:
        print(f'request:{request.method}')
        flash('Something Weird Happened!')
#        return redirect(request.url)
        return redirect('/failure/')


