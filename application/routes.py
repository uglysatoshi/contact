from application import app, db
from flask import render_template, request, redirect, url_for, session, flash
from datetime import datetime
from .forms import SellingForm
from bson import ObjectId


@app.route('/', methods=['POST', 'GET'])
def login():
    if "email" in session:
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = db.operators.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            password_check = email_found['password']
            if password == password_check:
                session["email"] = email_val
                return redirect(url_for('profile'))
            else:
                if "email" in session:
                    return redirect(url_for("profile"))
                flash("Неверный пароль или электронная почта", "Ошибка")
                return render_template('login.html')
        else:
            flash("Неверный пароль или электронная почта", "Ошибка")
            return render_template('login.html')
    return render_template('login.html')


@app.route('/profile', methods=['GET'])
def profile():
    if 'email' in session:
        operator = db.operators.find_one({'email': session['email']})
        return render_template('profile.html', operator=operator)
    else:
        flash("Необходимо войти в учетную запись", "Ошибка")
        return redirect('/')


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        flash("Выход из профиля совершен успешно", "Успех")
        return redirect(url_for('login'))
    else:
        flash("Необходимо войти в учетную запись", "Ошибка")
        return render_template('login.html')


@app.route("/seller", methods=["POST", "GET"])
def seller():
    if "email" in session:
        operator = db.operators.find_one({'email': session['email']})
        if operator["seller"]:
            sells = []
            for sell in db.sellings.find():
                sell["_id"] = str(sell["_id"])
                sells.append(sell)
            return render_template('seller.html', sells=sells)
        else:
            return render_template('zero_access.html')
    else:
        flash("Необходимо войти в учетную запись", "Ошибка")
        return redirect(url_for('login'))


@app.route("/add_selling", methods=["POST", "GET"])
def add_selling():
    if "email" in session:
        operator = db.operators.find_one({'email': session['email']})
        if operator["seller"]:
            if request.method == "POST":
                form = SellingForm(request.form)
                sell_name = form.item.data
                sell_status = form.status.data
                seller_firstname = operator["firstname"]
                seller_lastname = operator["lastname"]
                sell_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                db.sellings.insert_one({
                    "item": sell_name,
                    "date_created": sell_date,
                    "firstname_seller": seller_firstname,
                    "lastname_seller": seller_lastname,
                    "status": sell_status
                })
                flash("Продажа успешно добавлена", "Успех")
                return redirect(url_for('seller'))
            else:
                form = SellingForm()
                return render_template("add_selling.html", form=form)
        else:
            return render_template('zero_access.html')
    else:
        return redirect(url_for('login'))


@app.route('/edit/<db_item_id>', methods=["POST", "GET"])
def edit_selling(db_item_id):
    if "email" in session:
        operator = db.operators.find_one({'email': session['email']})
        if operator["seller"]:
            if request.method == "POST":
                delete_selling(db_item_id)
                form = SellingForm(request.form)
                sell_name = form.item.data
                sell_status = form.status.data
                seller_firstname = operator["firstname"]
                seller_lastname = operator["lastname"]
                sell_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
                db.sellings.insert_one({
                    "item": sell_name,
                    "date_created": sell_date,
                    "firstname_seller": seller_firstname,
                    "lastname_seller": seller_lastname,
                    "status": sell_status
                })
                flash("Продажа успешно отредактирована", "Успех")
                return redirect(url_for('seller'))
            else:
                form = SellingForm()
                item = db.sellings.find_one_or_404({"_id": ObjectId(db_item_id)})
                form.item.data = item.get("item", None)
                form.status.data = item.get("status", None)
                return render_template("add_selling.html", form=form)
        else:
            return render_template('zero_access.html')
    else:
        flash("Необходимо войти в учетную запись", "Ошибка")
        return redirect(url_for('login'))


@app.route("/delete/<db_item_id>")
def delete_selling(db_item_id):
    # calling a db and deleting item by _id
    db.sellings.find_one_and_delete({"_id": ObjectId(db_item_id)})
    flash("Продажа успешно удалена", "Успех")
    return redirect(url_for('seller'))


@app.route("/manager", methods=["GET"])
def manager():
    if "email" in session:
        operator = db.operators.find_one({'email': session['email']})
        if operator["manager"]:
            clients = []
            total_balance = 0
            total_purchases = 0
            for client in db.clients.find():
                client["_id"] = str(client["_id"])
                client["balance"] = round(client["balance"], 3)
                if client["balance"] > 0:
                    total_balance += client["balance"]
                total_purchases += client["purchases"]
                clients.append(client)
            total_balance = round(total_balance, 3)
            return render_template('manager.html',
                                   clients=clients,
                                   totalBalance=total_balance,
                                   totalPurchases=total_purchases)
        else:
            return render_template('zero_access.html')
    else:
        flash("Необходимо войти в учетную запись", "Ошибка")
        return redirect(url_for('login'))


@app.route("/manager/balance_descending", methods=["GET"])
def manager_balance_descending():
    if "email" in session:
        operator = db.operators.find_one({'email': session['email']})
        if operator["manager"]:
            clients = []
            total_balance = 0
            total_purchases = 0
            for client in db.clients.find().sort("balance", 1):
                client["_id"] = str(client["_id"])
                client["balance"] = round(client["balance"], 3)
                total_balance += client["balance"]
                total_purchases += client["purchases"]
                clients.append(client)
            total_balance = round(total_balance, 3)
            flash("Клиенты отсортированы по возрастанию баланса", "Успех")
            return render_template('manager.html',
                                   clients=clients,
                                   totalBalance=total_balance,
                                   totalPurchases=total_purchases)
        else:
            return render_template('zero_access.html')
    else:
        flash("Необходимо войти в учетную запись", "Ошибка")
        return redirect(url_for('login'))


@app.route("/manager/balance_ascending", methods=["GET"])
def manager_balance_ascending():
    if "email" in session:
        operator = db.operators.find_one({'email': session['email']})
        if operator["manager"]:
            clients = []
            total_balance = 0
            total_purchases = 0
            for client in db.clients.find().sort("balance", -1):
                client["_id"] = str(client["_id"])
                client["balance"] = round(client["balance"], 3)
                total_balance += client["balance"]
                total_purchases += client["purchases"]
                clients.append(client)
            total_balance = round(total_balance, 3)
            flash("Клиенты отсортированы по убыванию баланса", "Успех")
            return render_template('manager.html',
                                   clients=clients,
                                   totalBalance=total_balance,
                                   totalPurchases=total_purchases)
        else:
            return render_template('zero_access.html')
    else:
        flash("Необходимо войти в учетную запись", "Ошибка")
        return redirect(url_for('login'))
