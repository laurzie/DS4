from flask import Flask, request, render_template, flash, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, DateField, IntegerField, BooleanField, ValidationError # see some new ones... + ValidationError
from wtforms.validators import Required, Length, Email, Regexp
import json, requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug=True

API_KEY = "f5cef52dedb64f26b013bdb8175c0686"

class ZipcodeForm(FlaskForm):
    zipcode = StringField('Enter a US zipcode?', validators=[Required()])
    submit = SubmitField('Submit')

    def validate_zipcode(self, field):
        if len(str(field.data)) !=5:
            raise ValidationError("Your zipcode was not valid because there was either less than 5 numbers or more than 5 numbers.")


@app.route('/zipcode', methods = ["GET", "POST"])
def zipcode_view():
    form = ZipcodeForm()
    if form.validate_on_submit():
        zipcode = str(form.zipcode.data)
        params = {}
        params['zip'] = zipcode + ",us"
        params['appid'] = "f5cef52dedb64f26b013bdb8175c0686"
        baseurl = "http://api.openweathermap.org/data/2.5/weather?"
        response = requests.get(baseurl, params = params)
        response_dict = json.loads(response.text)

        description = response_dict["weather"][0]["description"]
        name = response_dict["name"]
        temp_kalvin = response_dict["main"]["temp"]

        return render_template("weather_results.html", description = description, city = name, temperature = temp_kalvin)

    flash(form.errors)
    return render_template("weather.html", form = form)

if __name__ == "__main__":
    app.run(debug=True)
