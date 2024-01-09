import hashlib
import json

from flask import render_template, redirect, url_for, request, make_response, jsonify
from itsdangerous import URLSafeTimedSerializer
from project import app, Session, Base, engine, config
from project.models import Users, Feature


def check_session(session_name):
    signed_session = request.cookies.get(session_name)
    username = None

    if signed_session:
        serializer = URLSafeTimedSerializer(app.secret_key)

        try:
            session_data = serializer.loads(signed_session)
            username = session_data.get("username")
            return username
        except Exception:
            return False

    return username


@app.route("/")
def index():
    with open("config.json", "r") as file:
        data = json.load(file)

    Base.metadata.create_all(bind=engine)
    main_text = data["web"]["main-text"]
    username = check_session("session")

    if username:
        with Session() as session:
            user_admin = session.query(Users).filter_by(username=username).first()

            if not user_admin.group == "admin":
                user_admin = None
    else:
        user_admin = None

    with Session() as session:
        features = session.query(Feature).all()

    return render_template(template_name_or_list="index.html",
                           username=username,
                           main_text=main_text,
                           user_admin=user_admin,
                           features=features)


@app.route("/admin/", methods=["POST", "GET"])
def admin():
    with open("config.json", "r") as file:
        data = json.load(file)

    signed_session = request.cookies.get("session")
    main_text = data["web"]["main-text"]

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

    with Session() as session:
        features = session.query(Feature).all()

    return render_template(template_name_or_list="admin.html",
                           username=username,
                           main_text=main_text,
                           features=features)


@app.route("/admin/add/feature/", methods=["POST"])
def add_feature():
    if request.method == "POST":
        feature_name = request.form.get("feature-name")
        feature_description = request.form.get("feature-description")
        feature_icon = request.form.get("feature-icon")

        with Session() as session:
            try:
                feature_object = Feature(
                    name=feature_name,
                    description=feature_description,
                    icon=feature_icon
                )
                session.add(feature_object)
                session.commit()
            except Exception as error:
                print(error)
                session.rollback()
                return redirect(url_for("admin"))

    return redirect(url_for("admin"))


@app.route("/admin/edit/main-text/", methods=["POST"])
def edit_main_text():
    if request.method == "POST":
        with open("config.json", "r") as file:
            data = json.load(file)

        main_text = request.form.get("main-text")

        data["web"]["main-text"] = main_text

        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)

    return redirect(url_for("admin"))


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
        username = check_session("session")

        if username:
            with Session() as session:
                user_admin = session.query(Users).filter_by(username=username).first()

                if not user_admin.group == "admin":
                    user_admin = None
        else:
            user_admin = None

        return render_template("sign-in.html", user_admin=user_admin)


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
        username = check_session("session")
        if username:
            with Session() as session:
                user_admin = session.query(Users).filter_by(username=username).first()

                if not user_admin.group == "admin":
                    user_admin = None
        else:
            user_admin = None

        return render_template("sign-up.html")


@app.route("/admin/get_feature_data/<int:feature_id>/", methods=["POST"])
def get_feature_info(feature_id):
    if request.method == "POST":
        with Session() as session:
            feature = session.query(Feature).filter_by(id=feature_id).first()

        if feature:
            return jsonify({
                "id": feature.id,
                "name": feature.name,
                "description": feature.description,
            })
        else:
            return jsonify({"error": "Feature not found"}), 404


@app.route("/admin/update_feature/<int:feature_id>/", methods=["POST"])
def update_feature(feature_id):
    if request.method == "POST":
        with Session() as session:
            feature = session.query(Feature).filter_by(id=feature_id).first()

            if feature:
                new_name = request.form.get("name")
                new_description = request.form.get("description")

                feature.name = new_name
                feature.description = new_description
                session.commit()
                return jsonify({"message": "Update successfully"})
            else:
                return jsonify({"error": "Feature not found"}), 404


@app.route("/admin/delete/feature/<int:feature_id>", methods=["POST"])
def delete_feature(feature_id):
    if request.method == "POST":
        with Session() as session:
            feature = session.query(Feature).filter_by(id=feature_id).first()

            if feature:
                try:
                    session.delete(feature)
                    session.commit()
                    return jsonify({"message": "Feature deleted successfully"})
                except Exception as error:
                    print(error)
                    return jsonify({"message": "Delete error"})


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
