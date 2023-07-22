from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3 as sql
import pandas as pd
import csv
import uuid
import random

app = Flask(__name__)

host = 'http://127.0.0.1:5000/'

conn = sql.connect("try2.db")
address_table = '''CREATE TABLE IF NOT EXISTS Address ( address_id TEXT PRIMARY KEY, zipcode TEXT, street_num TEXT, 
                street_name TEXT); '''
conn.execute(address_table)
address = pd.read_csv(r'C:\Users\yukih\Downloads\progress-v1-m\progress-v1-m\data\Address.csv')
address.to_sql(name='Address', con=conn, if_exists='replace', index=False)

buy_table = '''CREATE TABLE IF NOT EXISTS buy (email TEXT PRIMARY KEY, first_name TEXT, last_name TEXT, gender TEXT, 
age INTEGER, home_address_id TEXT, billing_address_id TEXT); '''
conn.execute(buy_table)
buyer = pd.read_csv(r'C:\Users\yukih\Downloads\progress-v1-m\progress-v1-m\data\Buyers.csv')
buyer.to_sql(name='buy', con=conn, if_exists='replace', index=False)
# buy = pd.DataFrame(buyer)

cate_table = '''CREATE TABLE IF NOT EXISTS cate (parent_category TEXT, category_name TEXT); '''
conn.execute(cate_table)
categor = pd.read_csv(r'C:\Users\yukih\Downloads\progress-v1-m\progress-v1-m\data\Categories.csv')
categor.to_sql(name='cate', con=conn, if_exists='replace', index=False)

cc_table = '''CREATE TABLE IF NOT EXISTS cc (credit_card_num TEXT PRIMARY KEY, card_code TEXT, expire_month TEXT, 
expire_year TEXT, card_type TEXT, Owner_email TEXT UNIQUE); '''
conn.execute(cc_table)
credit = pd.read_csv(r'C:\Users\yukih\Downloads\progress-v1-m\progress-v1-m\data\Credit_Cards.csv')
credit.to_sql(name='cc', con=conn, if_exists='replace', index=False)
# cc = pd.DataFrame(credit)

lv_table = '''CREATE TABLE IF NOT EXISTS lv (Email TEXT PRIMARY KEY, Business Name TEXT, Business Address ID TEXT, 
Customer Service Number TEXT); '''
conn.execute(lv_table)
Local = pd.read_csv(r'C:\Users\yukih\Downloads\progress-v1-m\progress-v1-m\data\Local_Vendors.csv')
Local.to_sql(name='lv', con=conn, if_exists='replace', index=False)

ord_table = '''CREATE TABLE IF NOT EXISTS ord (Transaction_ID INTEGER, Seller_Email TEXT, Listing_ID INTEGER, 
Buyer_Email TEXT, Date TEXT, Quantity INTEGER, Payment INTEGER); '''
conn.execute(ord_table)
order = pd.read_csv(r'C:\Users\yukih\Downloads\progress-v1-m\progress-v1-m\data\Orders.csv')
# ord = pd.DataFrame(order)
order.to_sql(name='ord', con=conn, if_exists='replace', index=False)

plist_table = '''CREATE TABLE IF NOT EXISTS plist (Seller_Email TEXT PRIMARY KEY, Listing_ID INTEGER PRIMARY KEY UNIQUE, 
Category TEXT, Title TEXT, subCategory_Name TEXT, subCategory_Description TEXT, Price TEXT, Quantity INTEGER NOT NULL); '''
conn.execute(plist_table)
subCategory = pd.read_csv(r'C:\Users\yukih\Downloads\progress-v1-m\progress-v1-m\data\Product_Listing.csv')
subCategory.to_sql(name='plist', con=conn, if_exists='replace', index=False)

r_table = '''CREATE TABLE IF NOT EXISTS r (Buyer_Email TEXT, Seller_Email TEXT, Date TEXT, 
Rating INTEGER, Rating_Desc TEXT); '''
conn.execute(r_table)
rating = pd.read_csv(r'C:\Users\yukih\Downloads\progress-v1-m\progress-v1-m\data\Ratings.csv')
rating.to_sql(name='r', con=conn, if_exists='replace', index=False)

re_table = '''CREATE TABLE IF NOT EXISTS re (Buyer_Email TEXT, Seller_Email TEXT, Listing_ID INTEGER, 
Review_Desc TEXT); '''
conn.execute(re_table)
review = pd.read_csv(r'C:\Users\yukih\Downloads\progress-v1-m\progress-v1-m\data\Reviews.csv')
re = pd.DataFrame(review)
review.to_sql(name='re', con=conn, if_exists='replace', index=False)

seller_table = '''CREATE TABLE IF NOT EXISTS sell (email TEXT PRIMARY KEY, routing_number TEXT, account_number INTEGER, 
balance INTEGER); '''
seller = pd.read_csv(r'C:\Users\yukih\Downloads\progress-v1-m\progress-v1-m\data\Sellers.csv')
seller.to_sql(name='sell', con=conn, if_exists='replace', index=False)

user_table = '''CREATE TABLE IF NOT EXISTS use (email TEXT PRIMARY KEY, password TEXT); '''
user = pd.read_csv(r'C:\Users\yukih\Downloads\progress-v1-m\progress-v1-m\data\Users.csv')
user.to_sql(name='use', con=conn, if_exists='replace', index=False)

conn.commit()

result=None
up=None
username=None
password=None
address=None
parent = 'Root'

# conn = sql.connect("data.db")
# conn.execute("CREATE TABLE IF NOT EXISTS user (email TEXT, password TEXT, PRIMARY KEY(email));")
#
# with open('C:\Users\yukih\Desktop\progress\data\Users.csv', 'r') as f:
#     for data in list(csv.reader(f))[1:]:
#         conn.execute("INSERT INTO user(email, password) VALUES (?,?);", data)
# cursor = conn.execute("SELECT * FROM user;")
# for _ in range(10):
#     print(next(cursor))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Home', methods=['POST', 'GET'])
def Home():
    global result
    signedInAs = signedInAs=result[0][1]+' '+result[0][2]
    print(signedInAs)
    return render_template('main.html', signedInAs=signedInAs)

@app.route('/login', methods=['POST', 'GET'])
def login():
    global result
    global username
    global password
    global address
    credit_card_num='1234-5678-9012-3456'
    print(len(credit_card_num))
    last_4_digit = credit_card_num[ len(credit_card_num) - 4 : len(credit_card_num) ]
    print(last_4_digit)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = sql.connect('try2.db')
        print("xx,yy11")
        print(username + ',' + password)
        # sw: added rowid to get the row number as the user ID or PID
        cursor = connection.execute('SELECT rowid, * FROM use WHERE email = ? AND password = ?', (username, password))

        # after above IF, we must found an user account matched the input username and password
        account = cursor.fetchall()
        if len(account) < 1:
            print("row count is 0")
            return render_template('index.html', error='Invalid username or password. Please try again.')
        print("xx,yy")

        # sw account is a list. Inside the list, the element is a tuple(email, password)
        result = account

        # find user's first name and last name
        cursor = connection.execute('SELECT * FROM buy WHERE email = ?', (username,))

        userInfo = cursor.fetchall()

        if len(userInfo) < 1:
            # buy table is not consistant with use table because there is no buyer with this email
            return render_template('index.html', error='buyers table does not contain username ' + username)
        address_id=userInfo[0][5]
        result = [(username, userInfo[0][1], userInfo[0][2], userInfo[0][3], userInfo[0][4])]
        print(result)
        signedInAs=result[0][1]+' '+result[0][2]
        print(signedInAs)
        print('address_id:', address_id)
        cursor = connection.execute('SELECT * FROM Address WHERE address_id = ?', (address_id,))
        address = cursor.fetchall()
        print(address)
        if len(address)<1:
            return render_template('index.html', error='Failed to find buyer '+username+' address')
        return render_template('main.html', signedInAs=signedInAs)

    # credit_num
    # last_4_digit=credit_num(len(credit_num)-4, len(credit_num))

@app.route('/CheckingInfo', methods=['POST','GET'])
def CheckingInfo():
    global result
    global up
    global address
    print('CheckingInfo:')
    print(result)
    up=[(username, password)]
    return render_template('CheckingInfo.html', error=None, result=result, up=up, address=address)

@app.route('/change', methods=['POST', 'GET'])
def change():
    global result
    global up
    global address
    if request.method == 'POST':
        username = request.form['username']
        oldpassword = request.form['oldpassword']
        newpassword = request.form['newpassword']
        connection = sql.connect('try2.db')
        print("xx,yy11")
        print(oldpassword + '' + newpassword)
        # sw: added rowid to get the row number as the user ID or PID
        cursor = connection.execute('SELECT rowid, * FROM use WHERE email = ? AND password = ?', (username,oldpassword))
        print("reach here?")
        # after above IF, we must found an user account matched the input username and password
        oldaccount = cursor.fetchall()
        if len(oldaccount) < 1:
            print("row count is 0")
            return render_template('CheckingInfo.html', error='Failed to change password. Invalid current password. Please try again.', result=result, up=up, address=address)
        print("xx????")

        # sw account is a list. Inside the list, the element is a tuple(email, password)
        #result = oldaccount

        # find user's first name and last name
        cursor = connection.execute('UPDATE use SET password = ? WHERE email = ?', (newpassword, username))
        password=newpassword
        print("here?")
        connection.commit()
        print("reach")

        cursor = connection.execute('SELECT * FROM use WHERE email = ?', (username,))
        userInfo = cursor.fetchall()
        print(userInfo)
        up = [(username, userInfo[0][1])]
        print('up:')
        print(up)
        print('result:')
        print(result)
        return render_template('CheckingInfo.html', error='Successfully changed password', result=result, up=up, address=address)

@app.route('/CategoryHierachy', methods=['POST', 'GET'])
def CategoryHierachy():
    connection = sql.connect('try2.db')

    tree = []

    # TODO: Need to spend some time to debug the following recursive() function to build
    # category tree dynamically from database
    # tree=recursive('Root', tree, connection)

    # For now, just hard-coded the category tree, will fix the bug later
    tree = [
        {'text': 'Root',
         'nodes': [
             {'text': 'Clothing',
              'nodes': [
                  {'text': 'Bodysuits',
                   'nodes': [
                       {'text': 'wlaurancegt@nsu.edu, Ribbed Turtleneck Bodysuit,$15, 4'},
                       {'text': 'nrideoutmi@nsu.edu, Ribbed Turtleneck Bodysuit, $120, 2'}
                   ]
                   },
                  {'text': 'Tops',
                   'nodes': [
                       {'text': 'ghalvorsen95@nsu.edu,Oversized T-shirt, $110, 0'},
                       {'text': 'awillderjq@nsu.edu, Oversized T-shirt, $110, 2'}
                   ]
                   },
                  {'text': 'Bottom'},
                  {'text': 'sleepwear',
                   'nodes': [
                       {'text': 'Bath Robes'}
                   ]}
              ]
              },
             {'text': 'Electrical Supplies',
              'nodes': [
                  {'text': 'Cell Phones'},
                  {'text': 'Tv & Home Theater',
                   'nodes':[
                       {'text':'75-Inch Tvs'},
                       {'text': '65-Inch Tvs'},
                       {'text': '55-Inch Tvs'}

                  ]},
                  {'text': 'Wearable Technology',
                   'nodes':[
                       {'text':'Apple Watch'},
                       {'text': 'HeadPhone'},
                       {'text': 'Wireless Headphones'}

                  ]},
              ]
              },
             {'text': 'Beauty Products',
              'nodes': [
                  {'text': 'Makeup',
                   'nodes': [
                       {'text': 'Face'},
                       {'text': 'Lip'},
                       {'text':'Brushes & Applicators'}
                   ]},

              ]
              },
             {'text': 'Kitchen & Appliances',
              'nodes': [
                  {'text': 'Kitchen & Cooking Accessories',
                   'nodes': [
                       {'text': 'Kitchen Utensils'},
                       {'text': 'Mixing & Measuring Tools'},
                       {'text': 'Cooking Accessories'}
                   ]},
                  {'text': 'Kitchen Cabinets',
                   'nodes':[
                       {'text':'Wall Cabinets'},
                       {'text': 'High Cabinets'},
                       {'text': 'Base Cabinets'},
                   ]},
                  {'text': 'Kitchen Faucets & Sinks',
                   'nodes': [
                       {'text': 'Kitchen Sinks'},
                       {'text': 'Kitchen Faucets'},
                   ]
                   }
              ]
              },
             {'text': 'Toys & Video Games',
              'nodes': [
                  {'text': 'Toys'},
                  {'text': 'Video Games'},
                  {'text': 'Outdoor play'}
              ]
              },
             {'text': 'Pharmacy, Health & Wellness',
              'nodes': [
                  {'text':'Health Care','nodes':[
                      {'text':'Cough, Cold & Flu'},
                      {'text': 'Pain Relievers'},
                      {'text': 'Eye Care'},
                  ]},
                  {'text':'Wellness','nodes':[
                      {'text':'Sleep Support'},
                      {'text': 'Performance Nutrition'},
                      {'text':'Weight Loss'}
                  ]}
              ]
              },
             {'text': 'Pets',
              'nodes': [
                  {'text': 'Cat',
                   'nodes':[
                       {'text':'Cat Dry Food'},
                       {'text': 'Cat Wet Food'},
                       {'text': 'Clmbing Tree'},
                  ]},
                  {'text': 'Dog',
                   'nodes':[
                      {'text': 'Dog Dry Food'},
                      {'text': 'Dog Wet Food'},
                       {'text':'Dog Bed'}
                  ]},

              ]
              },
             {'text': 'Sports & Outdoors',
              'nodes': [
                  {'text': 'Makeup'},
                  {'text': 'Face'},
                  {'text': 'Lip'}
              ]
              },
             {'text': 'Patio & Garden',
              'nodes': [
                  {'text': 'Makeup'},
                  {'text': 'Face'},
                  {'text': 'Lip'}
              ]
              },
             {'text': 'Grocery',
              'nodes': [
                  {'text': 'Bakery & Bread'},
                  {'text': 'Meat & Seafood'},
                  {'text': 'Fresh Product'}
              ]
              }
         ]
         }

    ]
    return render_template('category.html', data=tree)
def recursive(parent, tree, connection):
    t={'text':parent}
    cursor=connection.execute('SELECT * FROM cate WHERE parent_category = ?',(parent,))
    subCategory=cursor.fetchall();
    if (len(subCategory)>0):
        t['nodes'] = []
        for (p,c) in subCategory:
            t['nodes'].append(recursive(c,tree, connection))
        tree.append(t)
    else:
        cursor=connection.execute('SELECT * FROM plist WHERE Category = ?', (parent,))
        product=cursor.fetchall()
        print('product:')
        print(product)
        print(t)
        for (Seller_Email, Listing_ID , Category , Title , subCategory_Name , subCategory_Description , Price , Quantity) in product:
            t[0]['nodes'].append(Seller_Email+','+Listing_ID+','+Category+','+Title+','+subCategory_Name+','+subCategory_Description+','+Price+','+Quantity)
    tree.append(t)
    print(tree)
    return tree



@app.route('/SignOut', methods=['POST', 'GET'])
def SignOut():
    global username
    global password
    global result
    username = None
    password = None
    print('sign out')
    return render_template('index.html')

@app.route('/product', methods=['POST', 'GET'])
def product():
    global username
    global password
    global result
    connection = sql.connect('try2.db')
    cursor = connection.execute('SELECT rowid, * FROM use WHERE email = ? AND password = ?', (username, password))


if __name__ == "__main__":
    app.run(debug=True)
