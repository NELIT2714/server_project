import hashlib

from flask import render_template, redirect, url_for, request, make_response
from itsdangerous import URLSafeTimedSerializer
from project import app, Session, Base, engine, config
from project.models import Users


@app.route("/")
def index():
    Base.metadata.create_all(bind=engine)

    main_text = config["web"]["main-text"]

    signed_session = request.cookies.get("session")
    username = None

    if signed_session:
        serializer = URLSafeTimedSerializer(app.secret_key)

        try:
            session_data = serializer.loads(signed_session)
            username = session_data.get("username")
        except Exception as e:
            print(e)
            return 'Invalid session'

    return render_template("index.html", username=username, main_text=main_text)


@app.route("/admin/", methods=["POST", "GET"])
def admin():
    signed_session = request.cookies.get("session")
    username = None

    if signed_session:
        serializer = URLSafeTimedSerializer(app.secret_key)

        try:
            session_data = serializer.loads(signed_session)
            username = session_data.get("username")
        except Exception as e:
            print(e)
            return 'Invalid session'
    else:
        return redirect(url_for("index"))

    with Session() as session:
        user = session.query(Users).filter_by(username=username).first()

    if not user.group == "admin":
        return redirect(url_for("index"))

    return render_template("admin.html", username=username)


@app.route("/sign-in/", methods=["POST", "GET"])
def sign_in():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        with Session() as session:
            user = session.query(Users).filter_by(username=username).first()

            if user is None:
                user = session.query(Users).filter_by(email=username).first()

        if user is None:
            return "Takiego użytkownika nie ma"

        password_salted = password + config["web"]["salt"]
        password_hash = hashlib.md5()
        password_hash.update(password_salted.encode("utf-8"))

        if password_hash.hexdigest() == user.password:
            max_age = 7 * 24 * 60 * 60
            serializer = URLSafeTimedSerializer(app.secret_key)
            session_data = {"username": user.username}
            signed_session = serializer.dumps(session_data)
            response = make_response(redirect(url_for("index")))
            response.set_cookie("session", signed_session, max_age=max_age)

            return response
        else:
            return "Niepoprawne hasło, email lub nazwa użytkownika"
    else:
        signed_session = request.cookies.get("session")
        username = None

        if signed_session:
            serializer = URLSafeTimedSerializer(app.secret_key)

            try:
                session_data = serializer.loads(signed_session)
                username = session_data.get("username")
            except Exception as e:
                print(e)
                return 'Invalid session'

        if username:
            return redirect(url_for("index"))

        return render_template("sign-in.html")


@app.route("/sign-up/", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        full_name = request.form.get("full_name")
        email = request.form.get("full_name")
        password = request.form.get("password")
        password_2 = request.form.get("password_2")
        ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

        with Session() as session:
            user_username = session.query(Users).filter_by(username=username).first()
            user_email = session.query(Users).filter_by(email=email).first()

        if not user_username is None or user_username == config["web"]["super-admin"]["username"]:
            return "Nazwa użytkownika już jest zajęta"
        elif not user_email is None:
            return "Email juz jest zajęty"
        elif len(username) < 2 or len(username) > 16:
            return "Nazwa użytkownika nie może być dluższa niz 16 symboli i mniejsza niż 2"
        elif not password == password_2:
            return "Hasła nie są takie same"

        password_salted = password + config["web"]["salt"]

        password_hash = hashlib.md5()
        password_hash.update(password_salted.encode("utf-8"))

        with Session() as session:
            user_object = Users(
                username=username,
                full_name=full_name,
                email=email,
                password=password_hash.hexdigest(),
                register_ip=ip_addr
            )
            session.add(user_object)
            session.commit()

        max_age = 7 * 24 * 60 * 60
        serializer = URLSafeTimedSerializer(app.secret_key)
        session_data = {"username": username}
        signed_session = serializer.dumps(session_data)
        response = make_response(redirect(url_for("index")))
        response.set_cookie("session", signed_session, max_age=max_age)

        return response
    else:
        signed_session = request.cookies.get("session")
        username = None

        if signed_session:
            serializer = URLSafeTimedSerializer(app.secret_key)

            try:
                session_data = serializer.loads(signed_session)
                username = session_data.get("username")
            except Exception as e:
                print(e)
                return 'Invalid session'

        if username:
            return redirect(url_for("index"))

        return render_template("sign-up.html")


@app.route("/logout/")
def logout():
    response = make_response(redirect(url_for("index")))
    response.delete_cookie("session")
    return response


@app.route("/db/")
def drop_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return redirect(url_for("index"))
