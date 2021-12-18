import pyrebase

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

user = auth.sign_in_with_email_and_password("arman@gmail.com", "password")

print(user['idToken'])
