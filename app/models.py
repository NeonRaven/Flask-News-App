from app import db


class Article(db.Model):
    __tablename__ = 'Article'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(512), nullable=True)
    title = db.Column(db.String(1024), nullable=False)
    desc = db.Column(db.String(1024), nullable=True)
    author = db.Column(db.String(512), nullable=False)
    img = db.Column(db.String(1024), nullable=True)
    p_date = db.Column(db.DateTime, nullable=True)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Title {self.title}>'
