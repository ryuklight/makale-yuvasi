from flask import Flask, render_template, session, url_for, redirect, request, flash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, Form


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)

        else:
            flash("Bu sayfaya erişmeden önce giriş yapmalısınız!", "warning")
            return redirect(url_for("index"))

    return decorated_function



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////home/ryuk/PycharmProjects/makale-yuvasi/database.db'
app.config['SECRET_KEY'] = 'dosev'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25))
    last_name = db.Column(db.String(25))
    email = db.Column(db.String(50), unique=False)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(64))
    money = db.Column(db.Float)
    earned = db.Column(db.Float)
    verilmis_siparis_sayisi = db.Column(db.Integer)
    alinmis_siparis_sayisi = db.Column(db.Integer)
    toplam_kazanilan_para = db.Column(db.Float)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    words_count = db.Column(db.Integer)
    author = db.Column(db.String)
    category = db.Column(db.String)
    aciklama = db.Column(db.String)
    adet = db.Column(db.Integer)
    gun = db.Column(db.Integer)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    words_count = db.Column(db.Integer)
    author = db.Column(db.String)
    category = db.Column(db.String)
    price = db.Column(db.Float)




class RegisterForm(Form):
    username = StringField()
    password = PasswordField()
    confirm = PasswordField()
    email = StringField()
    first_name = StringField()
    last_name = StringField()

class LoginForm(Form):
    username = StringField()
    password = PasswordField()


@app.route('/')
def index():

    hazir_makaleler = Article.query.all()
    siparisler = Order.query.all()
    users = User.query.all()
    kullanici_sayisi = len(users)

    top_10 = list()
    liste2 = list()

    for i in users:
        liste2.append(i.earned)

    if kullanici_sayisi >= 10:
        for i in range(10):
            value = max(liste2)
            max_index = liste2.index(value)
            top_10.append(users[max_index])
            users.remove(users[max_index])
            liste2.remove(max_index)
    else:
        count = kullanici_sayisi
        for i in range(count):
            value = max(liste2)
            max_index = liste2.index(value)
            top_10.append(users[max_index])
            users.remove(users[max_index])
            liste2.remove(max_index)


    orders = list()

    first_loop = int(len(siparisler)/10) + 1

    for i in range(first_loop):
        liste = list()
        if len(siparisler) >= 10:
            for j in range(10):
                liste.append(siparisler[j])

            for x in range(10):
                siparisler.remove(siparisler[0])

            orders.append(liste)
        else:
            loop_count = len(siparisler)
            for j in range(loop_count):
                liste.append(siparisler[0])
                siparisler.remove(siparisler[0])

            orders.append(liste)

    print(orders)

    return render_template("index.html",anasayfa_aktif="active", iletiism_aktif="", makaleler_aktif="", siparisler_aktif="", makaleler=hazir_makaleler, siparisler=orders, top_10=top_10, page_number=1, session=session)





@app.route("/index/<string:id>")
def change_page(id):
    hazir_makaleler = Article.query.all()
    siparisler = Order.query.all()
    users = User.query.all()

    top_10 = list()
    liste2 = list()

    for i in users:
        liste2.append(i.earned)

    if len(users) >= 10:
        for i in range(10):
            value = max(liste2)
            max_index = liste2.index(value)
            top_10.append(users[max_index])
            users.remove(users[max_index])
            liste2.remove(max_index)
    else:
        pass


    orders = list()

    first_loop = int(len(siparisler)/10) + 1

    for i in range(first_loop):
        liste = list()
        if len(siparisler) >= 10:
            for j in range(10):
                liste.append(siparisler[j])

            for x in range(10):
                siparisler.remove(siparisler[0])

            orders.append(liste)
        else:
            loop_count = len(siparisler)
            for j in range(loop_count):
                liste.append(siparisler[0])
                siparisler.remove(siparisler[0])

            orders.append(liste)

    if int(id) > 0 and int(id) <= len(orders):
        return render_template("index.html", anasayfa_aktif="active", iletiism_aktif="", makaleler_aktif="", nasil_aktif="", makaleler=hazir_makaleler, siparisler=orders, top_10=top_10, page_number=int(id))

    else:
        return render_template("index.html", anasayfa_aktif="active", iletiism_aktif="", makaleler_aktif="", nasil_aktif="", makaleler=hazir_makaleler, siparisler=orders, top_10=top_10, page_number=1)





@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form

        username = form.get("username")
        password = form.get("password")

        result = User.query.filter_by(username=username).first()

        if result:
            user = result
            if user.password == password:
                session["id"] = user.id
                session["username"] = user.username
                session["password"] = user.password
                session["first_name"] = user.first_name
                session["last_name"] = user.last_name
                session["email"] = user.email
                session["money"] = user.money
                session["logged_in"] = True
                session["verilmis_siparis_sayisi"] = user.verilmis_siparis_sayisi
                session["alinmis_siparis_sayisi"] = user.alinmis_siparis_sayisi
                session["toplam_kazanilan_para"] = user.toplam_kazanilan_para



                flash("Başarıyla giriş yaptınız...","success")

                return redirect(url_for("index"))

            else:
                flash("Parola Yanlış!", "danger")
                return render_template("login.html",form=form)


        else:
            flash("Kullanıcı Bulunamadı!", "danger")
            return render_template("login.html",form=form)

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST":

        username = form.username.data
        password = form.password.data
        confirm = form.confirm.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        conditions = request.form.get("conditions")

        if conditions:

            result = User.query.filter_by(username=username).first()

            if result:
                flash("Bu kullanıcı adı kullanılıyor!", "danger")
                return render_template("register.html", form=form)

            elif password == confirm:


                newUser = User(first_name=first_name, last_name=last_name, email=email, username=username,
                               password=password, money=0.0, earned=0.0, verilmis_siparis_sayisi=0, alinmis_siparis_sayisi=0, toplam_kazanilan_para=0.0)
                db.session.add(newUser)
                db.session.commit()

                flash("Başarıyla kayıt oldunuz!", "success")

                login_form = LoginForm(username=username)
                return render_template("login.html",form=login_form)

            else:
                flash("Parolalar uyuşmuyor!","danger")
                return render_template("register.html", form=form)

        else:
            flash("Kayıt olabilmek için şartları kabul etmelisiniz!","danger")
            return render_template("register.html", form=form)

    else:
        return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Başarıyla Çıkış Yapıldı!", "primary")

    return redirect(url_for("index"))




@app.route("/control-panel")
@login_required
def control_panel():

    return render_template("control-panel.html",session=session,ozet_aktif="active",makale_ekle="",siparislerim="",hesap_ayarlari_aktif="",siparis_tamamla_aktif="")







if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
