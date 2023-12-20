from application import app, db
from flask import render_template, request, redirect, url_for, session, flash
from datetime import datetime
from .forms import SellingForm
from bson import ObjectId


@app.route('/', methods=['POST', 'GET'])
def login():
    message = 'Please login to your account'
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
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route('/profile', methods=['GET'])
def profile():
    if 'email' in session:
        operator = db.operators.find_one({'email': session['email']})
        return render_template('profile.html', operator=operator)
    else:
        return redirect('/')


@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return redirect(url_for('login'))
    else:
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
                sell_date = datetime.now().strftime("%d.%b.%Y %H:%M:%S")
                db.sellings.insert_one({
                    "item": sell_name,
                    "date_created": sell_date,
                    "firstname_seller": seller_firstname,
                    "lastname_seller": seller_lastname,
                    "status": sell_status
                })
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
                sell_date = datetime.now().strftime("%d.%b.%Y %H:%M:%S")
                db.sellings.insert_one({
                    "item": sell_name,
                    "date_created": sell_date,
                    "firstname_seller": seller_firstname,
                    "lastname_seller": seller_lastname,
                    "status": sell_status
                })
                flash("Продажа успешно отредактирована", "success")
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
        return redirect(url_for('login'))


@app.route("/delete/<db_item_id>")
def delete_selling(db_item_id):
    # calling a db and deleting item by _id
    db.sellings.find_one_and_delete({"_id": ObjectId(db_item_id)})
    flash("Selling is been deleted")
    return redirect(url_for('seller'))


@app.route("/manager", methods=["POST", "GET"])
def manager():
    if "email" in session:
        operator = db.operators.find_one({'email': session['email']})
        if operator["manager"]:
            return render_template('manager.html', operator=operator)
        else:
            return render_template('zero_access.html')
    else:
        return redirect(url_for('login'))