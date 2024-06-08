from flask import Flask, render_template, request, redirect, make_response
from pymongo import MongoClient
from functions import generate_id, send_email, find_id
import os

app = Flask('app')

client = MongoClient("mongodb+srv://orbitron324:LpopRFvlCG1GGX3Z@database.sch14ig.mongodb.net/?retryWrites=true&w=majority&appName=database")

db = client.Users
users = db.users

@app.route('/')
def home():
  id = request.cookies.get("id")
  logged_in = request.cookies.get("logged_in")

  if logged_in == "true":
    if id != None and find_id(users, id):
      return "You're logged in"

  return render_template('index.html')

@app.route('/signup')
def signup():
  id = request.cookies.get("id")
  logged_in = request.cookies.get("logged_in")

  if logged_in == "true":
    if id != None and find_id(users, id):
      document = users.find_one({"_id": id})

      email = document["email"]

      if document["verified"] == True:
        return redirect('/')

      return render_template('verify.html', email=email)
    
  return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
async def create_acc():
    id = request.cookies.get("id")
    logged_in = request.cookies.get("logged_in")

    if request.method == "POST":
        if logged_in == "true":
            if id is not None and await find_id(users, id):
                document = await users.find_one({"_id": id})

                if document:
                    code_1 = request.form.get("code_1")
                    code_2 = request.form.get("code_2")
                    code_3 = request.form.get("code_3")
                    code_4 = request.form.get("code_4")
                    code_5 = request.form.get("code_5")
                    code_6 = request.form.get("code_6")

                    if (str(code_1) + str(code_2) + str(code_3) + str(code_4) + str(code_5) + str(code_6) == str(document["verification_code"])):
                        await users.update_one({"_id": id}, {"$set": {"verified": True}})
                        return "You're verified buddy"

                    return render_template('verify.html', email=document["email"])

        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        age = request.form.get("age")

        document = {
            "_id": generate_id(12),
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "age": age,
            "roles": None,
            "verified": False,
            "enrolled": [],
            "verification_code": generate_id(6)
        }

        await users.insert_one(document)

        send_email("Verify your account", email, f"""Please verify your email address.

Use the following code to confirm your email address: {document["verification_code"]}

If you did not sign up for Codeminds, please ignore this email.

This is an automated message. Please do NOT reply to this email.

Thanks!""")

        resp = make_response(render_template('verify.html', email=email))
        resp.set_cookie("logged_in", "true")
        resp.set_cookie("id", document["_id"])

        return resp

    return redirect('/signup')


@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/about')
def hi():
  return list(users.find())

@app.route('/delete')
def e():
  for s in list(users.find()):
    if s['password'] == "testing":
      users.delete_one(s)

      resp = make_response("Success")
      resp.delete_cookie("logged_in")
      resp.delete_cookie("id")

      return resp
    
  return "Nope"

app.run(host='0.0.0.0', port=8080)
