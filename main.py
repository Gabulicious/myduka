from flask import Flask,render_template,request,redirect,url_for,flash,session
from dbservice import get_data,insert_products,insert_sales,sales_product,sales_pday,profit_product,register_user,check_email,check_email_pass
from flask_bcrypt import Bcrypt
#create the flask instance
app=Flask(__name__)

bcrypt=Bcrypt(app)

app.secret_key = b'Blackish360'

#first route
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/products')
def products():
    flash ("Login to Access products")
    if "email" not in session:
     return redirect(url_for ('login'))
    prods=get_data("products")
    # print(prods)
    return render_template("products.html",products=prods)

@app.route('/sales')
def sales(): 
    ("Login to access sales")
    if "email" not in session:
     return redirect(url_for ('login'))
    sales=get_data("sales")
    # print(sales)

    
    return render_template("sales.html",sales=sales)

@app.route('/register',methods=['POST','GET'])
def register(): 
    if request.method=="POST":
        # get )form data
        fname =request.form['name']
        email=request.form['email']
        password=request.form['password']
        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        x=check_email(email)
        if x==None:
        # insert user
            new_user=(fname,email,hashed_password)
            register_user(new_user)
            return redirect(url_for('login'))
        else:
            flash("Email already Exists")

            return redirect(url_for('login'))
  
    return render_template("register.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        
        email=request.form['email']
        password=request.form['password']
        user=check_email(email)

        if user==None:
            flash('Email does not exist')
            return redirect(url_for('register'))
        else:
            # check  password
            if bcrypt.check_password_hash(user[-1],password):
                flash('Login Successful')
                session['email']=email
                return redirect(url_for('dashboard'))

              
                # return redirect(url_for ('login'))
            else:
               flash('Incorrect Password')
        

    return render_template('login.html')






@app.route('/dashboard')
def dashboard():
    if "email" not in session:
     return redirect(url_for ('login'))
    s_product=sales_product()
    p_product=profit_product()
    s_day=sales_pday()
    print(s_day)
    
    print(p_product)
    
    print(s_product)
    names=[]
    sales=[]
    profit=[]
    day=[]
    for i in s_product:
        names.append(i[0])
        sales.append(float(i[1]))
    for i in p_product:
            names.append(i[0])
            profit.append((i[1]))
    for i in s_day:
        day.append(str(i[0]))
        sales.append(float(i[1]))
    return render_template("dashboard.html",names=names,sales=sales,profit=profit,day=day)

@app.route('/add_products',methods=['POST','GET'])

def add_products():
    if request.method=='POST':
    # request data from form
     pid=request.form['product_id']
     pname=request.form['product_name']
     bprice=request.form['buying_price']
     sprice=request.form['selling_price']
     squantity=request.form['stock_quantity']
    # insert products
     new_prods=(pid,pname,bprice,sprice,squantity)
     insert_products(new_prods)
     return redirect(url_for('products'))
    

@app.route('/make_sale',methods=["POST,GET"])
def make_sale():
    # check the method
    if request.method=='POST':
        # request data
        pid=request.form['pid']
        quantity=request.form['quantity']
        # insert sale
        new_sale=(pid,quantity)
        insert_sales(new_sale)
        return redirect(url_for('sales'))
    
@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect(url_for('login'))



##task
#create 3 html files  and ensure all html files are bs enabled
#products.html,sales.html,dashboard.html
#render the html files
#create the dashboard route
app.run(debug=True)