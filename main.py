from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os
import smtplib
from email.message import EmailMessage


class ContactForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    message = StringField('message', validators=[DataRequired()])
    submit = SubmitField('submit')


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)
my_email = 'hayward.m.rob@gmail.com'
my_password = 'fxjodsekabnvlhbj'


@app.route('/', methods=['GET', 'POST'])
def home():
    name = None
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        msg = EmailMessage()
        msg['From'] = form.email.data
        msg['To'] = my_email
        msg['Subject'] = 'robhayward.io enquiry'
        msg.set_content(f'name: {name}\nemail: {email}\nmessage: {message}')
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(my_email, my_password)

            smtp.send_message(msg)
            smtp.quit()
        form.name.data = ''
    return render_template('index.html', name=name, form=form)


if __name__ == '__main__':
    app.run(debug=True)
