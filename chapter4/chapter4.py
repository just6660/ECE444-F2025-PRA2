from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev"

bootstrap = Bootstrap5(app)


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField(
        "What is your UofT Email Address",
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        email = form.email.data.strip()

        old_name = session.get("name")
        if old_name and old_name != form.name.data:
            flash("Looks like you have changed your name!")

        if "utoronto" in email.lower():
            session["name"] = name
            session["email"] = email
            flash("UofT email verified. Welcome!", "success")
        else:
            flash(
                'Please use your UofT email address (must contain "utoronto").',
                "warning",
            )

        return redirect(url_for("index"))
    return render_template(
        "index.html", form=form, name=session.get("name"), email=session.get("email")
    )


if __name__ == "__main__":
    app.run(debug=True)
