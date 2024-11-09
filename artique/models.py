from artique import db

class User(db.Model):
    #primary key
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(200), unique= True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    nickname = db.Column(db.String(200), unique=True, nullable=False)

    # User 테이블에서 user.picture_set << 이런 식으로 그림 테이블 접근 가능.


class Picture(db.Model):
    #primary key
    id = db.Column(db.Integer, primary_key=True)

    # foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', name='fk_picture_user_id_user'))
    user = db.relationship('User', backref=db.backref('picture_set'))

    name = db.Column(db.String(200))
    artist = db.Column(db.String(200))
    gallery = db.Column(db.String(200))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    custom_prompt = db.Column(db.Text)
    custom_explanation = db.Column(db.Text, nullable=False)
    custom_question = db.Column(db.Text)
    sound = db.Column(db.String(500)) #음악파일은 외부 스토리지에 저장하고 url만 저장
    picture_photo = db.Column(db.String(500)) #사진은 외부 스토리지에 저장하고 url만 저장


class Chat(db.Model):
    #primary key
    id = db.Column(db.Integer, primary_key=True)

    #foreign key
    picture_id = db.Column(db.Integer, db.ForeignKey('picture.id', name='fk_chat_picture_id_picture'))
    picture = db.relationship('Picture', backref=db.backref('chat_set'))

    message = db.Column(db.Text)
    sender = db.Column(db.String(200))
    receiver = db.Column(db.String(200))


class Sentence(db.Model):
    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id', name='fk_sentence_chat_id_chat'))
    chat = db.relationship('Chat', backref=db.backref('sentence_set'))

    receiver_id = db.Column(db.Integer)
    summary = db.Column(db.Text)