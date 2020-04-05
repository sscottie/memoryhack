from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField(_l('Имя пользователя'), validators=[DataRequired()])
    about_me = TextAreaField(_l('О себе'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Сохранить'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Имя занято.'))


class PostForm(FlaskForm):
    post = TextAreaField(_l('Текст под Word2Vec'), validators=[DataRequired()])
    submit = SubmitField(_l('Подтвердить'))


class SearchForm(FlaskForm):
    q = StringField(_l('Поиск'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Текст сообщения'), validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Отправить'))
