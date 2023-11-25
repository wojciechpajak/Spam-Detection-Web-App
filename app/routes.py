from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, ClassificationForm, UpdateAccountForm
from app.models import User, RateHistory, Model
from app.classification import Classification
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
@app.route("/home")
def home():
    metric_mnb = Model.query.filter_by(id=1).first()
    metric_svc = Model.query.filter_by(id=2).first()
    metric_mlp = Model.query.filter_by(id=3).first()
    return render_template('home.html', title='Opis', metric_mnb=metric_mnb, metric_svc=metric_svc, metric_mlp=metric_mlp)


@app.route("/project", methods=['GET', 'POST'])
def project():
    form = ClassificationForm()
    text, model = None, None
    classifier = None
    prediction_class, prediction_ham, prediction_spam, shap_plot = None, None, None, None

    if form.validate_on_submit():
        input = [str(form.content.data)]
        text = str(form.content.data)
        model = form.model.data
        classifier = Classification(input, model)
        prediction_class = classifier.get_class_prediction()
        prediction_ham = classifier.get_ham_prediction()
        prediction_spam = classifier.get_spam_prediction()
        shap_plot = classifier.text_plot()
        if form.save.data:
            record = RateHistory(content=text, model=model, rate=prediction_class, ham_rate=prediction_ham, 
                                    spam_rate=prediction_spam, plot=shap_plot, user=current_user)
            db.session.add(record)
            db.session.commit()
            flash('Zapisano pomyślnie!', 'success')

    return render_template('project.html', 
                           form=form, prediction_class=prediction_class, prediction_ham=prediction_ham, 
                           prediction_spam=prediction_spam, shap_plot=shap_plot
                           )


@app.route("/demo", methods=['GET', 'POST'])
def demo():
    form = ClassificationForm()
    input, model = None, None
    classifier = None
    prediction_class, prediction_ham, prediction_spam, shap_plot = None, None, None, None
    dict = {
        'spam': 'Hi, Thanks for working with us. Your bill for $373,75 was due on 28 Dec 2023. If you have already paid if, please ignore this email and sorry for bothering you. If you have not paid it, please do so as soon as possible. To view your bill visit http://in.xero.com/1DOKskaWDK39ad1wd02. If you have got any questions, or want to arrange alternative payment do not hesitate to get in touch. Thanks', 
        'ham': 'Dear Chief Officer Alex, I hope this email finds you well. I am writing to inform you of a health issue that requires me to take a day off tomorrow. I have informed Mr. Mahone, and he suggested that I reach out to you to discuss a potential adjustment to my work arrangements. I am committed to ensuring our work progresses smoothly and am willing to collaborate on alternative solutions. I can provide necessary documentation to support this request. Please let me know when it would be convenient to discuss this further. Thank you for your understanding. Best regards, Michael'
        }
    example = dict
    form.content.data = dict[str(form.select.data)]

    if form.validate_on_submit():
        input = [str(form.content.data)]
        model = form.model.data
        classifier = Classification(input, model)
        prediction_class = classifier.get_class_prediction()
        prediction_ham = classifier.get_ham_prediction()
        prediction_spam = classifier.get_spam_prediction()
        shap_plot = classifier.text_plot()

    return render_template('demo.html', title='Demo',
                           form=form, example=example, prediction_class=prediction_class, prediction_ham=prediction_ham, 
                           prediction_spam=prediction_spam, shap_plot=shap_plot
                           )


@app.route("/history")
@login_required
def history():
    history = RateHistory.query.filter_by(user_id=current_user.id)
    return render_template('history.html', title='Historia', history=history)


@app.route("/history/<record_id>")
@login_required
def record(record_id):
    record = RateHistory.query.get_or_404(record_id)    # Jeśli post nie istnieje zwraca 404
    metric = Model.query.filter_by(name=record.model).first()
    return render_template('record.html', record=record, metric=metric)


@app.route("/history/<record_id>/delete", methods=['GET', 'POST'])
@login_required
def delete(record_id):
    record = RateHistory.query.get_or_404(record_id)    # Jeśli post nie istnieje zwraca 404
    if record.user != current_user:
        abort(403)
    db.session.delete(record)
    db.session.commit()
    flash(f'Pomyślnie usunięto zapis!', 'success')
    return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Pomyślnie utworzono konto dla {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Utwórz konto', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Nie ma takiego konta.', 'danger')
    return render_template('login.html', title='Zaloguj', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Zapisano pomyślnie!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data == current_user.username
        form.email.data == current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Konto', image_file=image_file, form=form)

