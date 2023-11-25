from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class MinWords(object):
    def __init__(self, message=None, min=1):
        if message is None:
            message = f'Pole musi zawierać co najmniej {min} słów (nie licząc słów z tzw. stop listy).'
        self.message = message
        self.min = min

    def __call__(self, form, field):
        text = field.data
        stopword = stopwords.words('english')
        email_stopword = stopword.copy()
        email_stopword.remove("re")
        text = re.sub(r'(\d+)', r' \1 ', text)
        tokens = word_tokenize(text)
        new_tokens = []
        num_tag = 'NUMBER'
        for token in tokens:
            if token.isdigit():
                new_tokens.append('NUMBER')
            elif token not in email_stopword and token is not num_tag:
                token.lower()
                new_tokens.append(token)
        length = len(new_tokens)
        if field.data:
            if length < self.min:
                raise ValidationError(self.message)


class ClassificationForm(FlaskForm):
    content = TextAreaField('Wiadomość e-mail:', render_kw={"rows": 8, "cols": 100}, validators=[DataRequired(), MinWords(min=10)])
    submit = SubmitField('Analizuj')
    save = SubmitField('Zapisz')
    model_choices = [("MNB_EnronAll_MaxFeatures1000", "Multinomial Naive Bayes"), ("SVC_EnronAll_MaxFeatures1000", "C-Support Vector"), ("MLP_EnronAll_MaxFeatures1000", "Multi-layer Perceptron")]
    model = SelectField('Klasyfikator:', choices=model_choices, validators=[DataRequired()])

    examples = [("spam", "Spam"), ("ham", "Ham")]
    select = SelectField('Wybierz typ wiadomości e-mail:', choices=examples, validators=[DataRequired()], default="spam")


class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Utwórz konto')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Nazwa użytkownika niedostępna.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ten email należy już do istniejącego konta.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class UpdateAccountForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Zapisz')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Nazwa użytkownika niedostępna.')
        elif username.data == current_user.username:
            raise ValidationError('Wprowadzono starą nazwę użytkownika.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Ten email należy już do istniejącego konta.')
        elif email.data == current_user.email:
            raise ValidationError('Wprowadzono stary adres email.')
