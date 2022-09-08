import sqlalchemy

from app import db

from sqlalchemy import Column, ForeignKey, Integer, Table, MetaData, create_engine, UniqueConstraint, \
    ForeignKeyConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

article_tag_association = Table(
    "article_tag",
    # Base.metadata,
    db.Model.metadata,
    Column("tag_id", ForeignKey("tag.id")),
    Column("article_id", ForeignKey("article.id"), index=True),
    UniqueConstraint('tag_id', 'article_id', name='unique_article_tag')
)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    #    source = db.Column(db.String(512), nullable=True)
    title = db.Column(db.String(1024), nullable=False)
    desc = db.Column(db.String(1024), nullable=True)
    author = db.Column(db.String(512), nullable=False)
    img = db.Column(db.String(1024), nullable=True)
    p_date = db.Column(db.DateTime, nullable=True)
    content = db.Column(db.Text, nullable=False)
    pub_id = Column(Integer, ForeignKey("publisher.id"))
    publisher = relationship("Publisher")
    tag_id = Column(Integer, ForeignKey("tag.id"))
    # tag = relationship("Tag")

    art_tags = relationship(
        "Tag",
        secondary=article_tag_association,
        # back_populates='articles'
        # primaryjoin=id == Article_Tag.c.article_id,
        # secondaryjoin=Tag.id == Article_Tag.c.tag_id
    )


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(512), nullable=True)

    tag_arts = relationship(
        "Article",
        secondary=article_tag_association,
        # back_populates='tags'
        # primaryjoin=id == Article_Tag.c.tag_id
    )


"""
class Article_Tag(db.Model):
    __tablename__ = 'article_tag'
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(ForeignKey("Tag.id"))
    article_id = db.Column(ForeignKey("Article.id"))

"""


class Publisher(db.Model):
    __tablename__ = 'publisher'
    id = db.Column(db.Integer, primary_key=True)
    publisher = db.Column(db.String(512), nullable=True)
    country = db.Column(db.String(512), nullable=True)
    about = db.Column(db.String(512), nullable=True)
    logo_path = db.Column(db.String(512), nullable=True)
    tweeter_handle = db.Column(db.String(512), nullable=True)


'''
tag_arts = relationship(
    "Articles", secondary=Article_Tag, back_populates="art_tags"
)
art_tags = relationship(
    "Tags", secondary=Article_Tag, back_populates="tag_arts"
)
'''

db.create_all()
db.session.commit()


def create_test_data():

    #neutrals
    pb = Publisher(publisher="Global Association of Journalists (GAJ)",
                   about="Global Association of Journalists (GAJ) is a global consortium of journalists. It is not country-specific and aims for a neutral tone.",
                   tweeter_handle='GAJ'
                   )
    db.session.add(pb)

    pb = Publisher(publisher="Humfeed News",
                   about="For celebrity gossip, information, and tech!",
                   tweeter_handle='humfeed'
                   )
    db.session.add(pb)

    #kam
    entry = Publisher(publisher="Kamarian Daily News",
                      about="Kamarian Daily News is an excellent news source, focused on the bigger picture.",
                      country="kam",
                      tweeter_handle='KamDaily'
                      )

    db.session.add(entry)

    entry2 = Publisher(publisher="Kamabart",
                      about="Kamabart. We know the actual truth",
                      country="kam",
                      tweeter_handle='Kamabart')
    db.session.add(entry2)


    #li
    entry3 = Publisher(publisher="The Longie Way",
                      about="The Longie Way, Longway Island's Daily Source of Truth.",
                      country="li",
                      tweeter_handle='LongieWay')
    db.session.add(entry3)

    entry4 = Publisher(publisher="LIBC",
                      about="Longway Island Broadcasting Corporation).",
                      country="li",
                      tweeter_handle='LIBC')
    db.session.add(entry4)

    entry5 = Publisher(publisher="The National Viewpoint",
                      about="The National Viewpoint. Australian. Balanced. Opinionated.",
                      country="au",
                      tweeter_handle='NatView')
    db.session.add(entry5)

    entry6 = Publisher(publisher="The Australian Post",
                      about="The Australian Post - Australia's largest trusted news source",
                      country="au",
                      tweeter_handle='AUSPost')
    db.session.add(entry6)



    taglist = ['Weather', 'News', 'Science', 'Technology',
               'History', 'Places', 'Entertainment', 'Health', 'Military',
               'Politics', 'Celebrity', 'Disaster']

    for tag in taglist:
        tg = Tag(tag=tag)
        db.session.add(tg)
        db.session.commit()

    new_story = Article(
        #    source = db.Column(db.String(512), nullable=True)
        title="Who Let The Dogs Out?",
        desc="have we yet discovered who let the dogs out?",
        author="Lance Armstrong",
        img="/assets/img/1.jpg",
        p_date="2022-11-11 11:11:11",
        content="It was I",
        pub_id=1,

#        tag_id=1
    )

    tgs =[]
    tgs.append( Tag.query.filter_by(id=1).first())
    tgs.append( Tag.query.filter_by(id=2).first())
    new_story.art_tags = tgs

    db.session.add(new_story)



    """
    a1 = sqlalchemy.insert(Article_Tag).values(tag_id=1, article_id=1)
    db.session.add(a1)
"""
    db.session.commit()
