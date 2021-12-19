import datetime
from os import name
import json
from flask import *  
import pyrebase
import ast
config = {
    "apiKey": "AIzaSyCg4U026dC23tr0anVQIB3lyIg_-grc6Ak",
  "authDomain": "hackathon-3dc95.firebaseapp.com",
  "projectId": "hackathon-3dc95",
  "storageBucket": "hackathon-3dc95.appspot.com",
  "messagingSenderId": "242647933043",
  "appId": "1:242647933043:web:87f2639e8f4e71f39e4a06",
  "measurementId": "G-H2QPZR2PBG",
  "databaseURL" : "https://hackathon-3dc95-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__)  

#Home route
@app.route('/')
def home():
    return render_template("onpg.html")

@app.route('/loginpage')
def loginpage():
    return render_template("login.html")

@app.route('/registerpage')
def registerpage():
    return render_template("registration.html")

@app.route('/searchpage')
def searchpage():
    return render_template("search.html")


@app.route('/respage',methods = ['POST'])
def respage():
    if request.method == 'POST':
        uid = request.form['uid']
        data = request.form['data']
        datatime_book = request.form['datetime_book']
        seats = request.form['seats']
        data = ast.literal_eval(data)
        seats_available = data[datatime_book]
        return render_template("res.html",data = {"uid":uid,"value":data,"seats":seats_available,"seats_tobook":seats,"datatime_book":datatime_book})

#Login route
@app.route('/login',methods = ['POST'])  
def login():  
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            customer = db.child("users").child(user['localId']).get()
            name = customer.val()["name"]
            return render_template("search.html", data = {"id" : user['localId'], "name": name})
        except:
            return {"auth" : False, "msg":"Invalid Credentials"}
    else:
        return {"auth":"Something is wrong"}

@app.route('/loginscreen',methods = ['POST'])  
def loginscreen():  
    if request.method == 'POST':
        uid = request.form['uid']
        try:
            customer = db.child("users").child(uid).get()
            name = customer.val()["name"]
            return render_template("search.html", data = {"id" : uid, "name": name})
        except:
            return {"auth" : False, "msg":"Invalid Credentials"}
    else:
        return {"auth":"Something is wrong"}


#register route
@app.route('/register',methods = ['POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        user = 'arman'
        try:
            user = auth.create_user_with_email_and_password(email,password)
            data = {
                "name":name,
                "booked_seats" : [0,]
            }
            results = db.child("users").child(user['localId']).set(data)
            return render_template("search.html", data = {"id" : user['localId'], "name": name})
        except:
            return {"auth" : False, "msg":"Email ID already registered"}
    else:
        return {"auth":"Something is wrong"}

#search resto
@app.route('/search',methods = ['POST'])
def search():
    if request.method == 'POST':
        users = db.child("resto_list").get()
        date = request.form['date']
        time = request.form['time']
        place = request.form['place']
        seats = request.form['seats']
        uid = request.form['uid']
        available = []
        for i in users.val():
            if i!=None and i[date+time] >= int(seats) and place.lower() in i['address'].lower():
                available.append(i)
        if(len(available)!=0):     
            return render_template("list.html", data = {"value":available,"uid" : uid,"datetime_book":date+time,"seats":seats})
            
        else:
            return {'msg':'No restaurents found'}


#booking seats
@app.route('/book',methods = ['POST'])
def book():
    if request.method == 'POST':
        uid = request.form['uid']
        resto_name = request.form['resto_name']
        resto_add = request.form['resto_add']
        seats = request.form['seats']
        datetime = request.form['datetime']
        users = db.child("resto_list").get()
        customer = db.child("users").child(uid).get()
        old_tickets = customer.val()['booked_seats']
        for i in users.val():
            if i!=None and i["name"]==resto_name and i["address"] == resto_add and i[datetime] >= int(seats):
                data = {
                    "name" : i["name"],
                    "address" : i["address"],
                    "reviews": i['reviews'],
                    "total_seats":i["total_seats"],
                    datetime : i[datetime]-int(seats)
                }
                index = users.val().index(i)
                db.child("resto_list").child(index).update(data)
                instance_found = 0
                for j in old_tickets:
                    if j!=0 and j!=None and j["name"]==resto_name and j["address"] == resto_add and j['datetime'] == datetime:
                        order_data = {
                            "name" : j["name"],
                            "address" : j["address"],
                            "seats" : int(j['seats'])+int(seats),
                            "datetime" : j['datetime']
                        }
                        old_index = old_tickets.index(j)
                        db.child("users").child(uid).child("booked_seats").child(old_index).update(order_data)
                        instance_found = 1
                if instance_found == 0:
                    order_data = {
                    "name" : i["name"],
                    "address" : i["address"],
                    "seats" : seats,
                    "datetime" : datetime
                    }
                    old_tickets.append(order_data)
                    customer_data = {
                        "name" : customer.val()['name'],
                        "booked_seats" : old_tickets
                    }
                    customer = db.child("users").child(uid).update(customer_data)
        return render_template("thank_you_cancel.html",data = {"msg":"Succesfully booked your tickets","uid":uid,"secmsg":"Click the button below to go to the search page"})

#cancel order
@app.route('/cancel',methods = ['POST'])
def cancel():
    if request.method == 'POST':
        uid = request.form['uid']
        resto_name = request.form['resto_name']
        resto_add = request.form['resto_add']
        seats = request.form['seats']
        datetime = request.form['datetime']
        users = db.child("resto_list").get()
        customer = db.child("users").child(uid).get()
        old_tickets = customer.val()['booked_seats']
        name = customer.val()['name']
        print(old_tickets)
        for i in users.val():
            if i!=None and i["name"]==resto_name and i["address"] == resto_add:
                data = {
                    "name" : i["name"],
                    "address" : i["address"],
                    "reviews": i['reviews'],
                    "total_seats":i["total_seats"],
                    datetime : i[datetime]+int(seats)
                }
                index = users.val().index(i)
                for j in old_tickets:
                    if j!=0 and j!=None and j["name"]==resto_name and j["address"] == resto_add and j['datetime'] == datetime and int(j["seats"]) >= int(seats):
                        order_data = {
                                        "name" : j["name"],
                                        "address" : j["address"],
                                        "seats" : int(j["seats"])-int(seats),
                                        "datetime" : datetime
                                    }
                        old_index = old_tickets.index(j)
                        db.child("users").child(uid).child("booked_seats").child(old_index).update(order_data)
                        db.child("resto_list").child(index).update(data)
                        return render_template("thank_you_cancel.html",data = {"msg":"Succesfully cancelled your tickets","uid":uid,"name":name,"secmsg":"Click the button below to go to the my bookings page"})

#mybookings
@app.route('/mybookings',methods = ['POST'])
def mybookings():
    if request.method == 'POST':
        uid = request.form['uid']
        customer = db.child("users").child(uid).get()
        name = customer.val()['name']
        old_tickets = customer.val()['booked_seats']
        bookings = []
        for k in old_tickets:
            if k!=0 and k!= None:
                bookings.append(k)
        return render_template("bookings.html", data = {"value":bookings,"name":name,"uid":uid})

#give reviews
@app.route('/reviews',methods = ['POST'])
def reviews():
    if request.method == 'POST':
        resto_name = request.form['resto_name']
        resto_add = request.form['resto_add']
        reviews = request.form['reviews']
        users = db.child("resto_list").get()
        for i in users.val():
            if i!=None and i["name"]==resto_name and i["address"] == resto_add:
                i['reviews'] = (int(i['reviews']) + int(reviews))/2
                index = users.val().index(i)
                db.child("resto_list").child(index).update(i)
                return {"msg":"success"}


if __name__ == '__main__':  
   app.run(debug = True)  