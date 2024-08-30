import psycopg2

#connect to database

conn=psycopg2.connect(
    dbname="myduka",
    user="postgres",
    host="localhost",
    password="Blackish360",
    port=5432
)

#cursor perform database operation

cur=conn.cursor()

#fetch products
def get_products():
    query="select * from products"
    cur.execute(query)
    products=cur.fetchall()
    return products

# get_products()

# fetch sales
def get_sales():
    query="select* from sales"
    cur.execute(query)
    sales=cur.fetchall()
    return sales



# get_sales()    


#create a function to fetch all data from db
#it will always be fetching data from db
#it should have a parameter
#FETCH SALES AND PRODUCTS USING THAT FUNCTION


def get_data(table):
    query=f"select * from {table}"
    cur.execute(query)
    data=cur.fetchall()
    return data

    

#get_data("products")

#insert
##products
# def insert_products():
#     query="insert into products(id,name,buying_price,selling_price,stock_quantity)\
#         values('5','fridge','100000','120000',20)"
#     cur.execute(query)
#     conn.commit()

# insert_products()
# get_data("products")

##sales
# def insert_sales():
#     query="insert into sales(id,pid,quantity,created_at)\
#         values('4','3','10',now())"
#     cur.execute(query)
#     conn.commit()

# insert_sales()
# get_data("sales")

#create 1 function to insert data to each table
#the function should be able to insert multiple data
#it should have parameters
#insert 2 products and make 4 sales

def insert_products(values):
    query="insert into products(id,name,buying_price,selling_price,stock_quantity)\
        values(%s,%s,%s,%s,%s)"#place holder
    cur.execute(query,values)
    conn.commit

# x=(7,"biscuits",200,300,19)
# insert_products(x)
# get_data("products")


def insert_sales(figures):
    query="insert into sales(id,pid,quantity,created_at)\
          values(%s,%s,%s,now())"
    cur.execute(query,figures)
    conn.commit

# y= (5,5,10)
# insert_sales(y)
# get_data("sales")


#write a query to get sales per product

def sales_product():
    query="select products.name, sum(sales.quantity* products.selling_price)\
          as sales_per_product from( sales INNER JOIN products on sales.pid=products.id) group by products.name;"

    cur.execute(query)
    data=cur.fetchall()
    return data

# sales_product()

##task
#1.write a query to display sales per day psql=>function on dbservice
def sales_pday():
    query="select date(sales.created_at) as day,sum(sales.quantity* products.selling_price)\
          as sales_per_day from(sales join products on sales.pid=products.id) group by sales.created_at order by day;"
    
    cur.execute(query)
    data=cur.fetchall()
    return data

# sales_pday()    

#2.write a query to display profit per product psql=>function on dbservice.py
def profit_product():
    query="select products.name, sum((products.selling_price -products.buying_price)*quantity)\
        as profit_per_product from (sales join products on sales.pid=products.id) group by products.name;"
    cur.execute(query)
    data=cur.fetchall()
    
    return data

# profit_product()

#3.write a query to display profit per day psql=>function on dbservice.py
# def profit_day():
#     query="select sales.created_at,sum((products.selling_price -products.buying_price) *sales.quantity)\
#           as profit_per_day from(sales join products on sales.pid=products.id) group by created_at;"
#     cur.execute(query)
#     data=cur.fetchall()
#     print(data)

# profit_day()

##inserting user
def register_user(values):
    query="insert into users(full_name,email,password)values(%s,%s,%s)"
        
    cur.execute(query,values)
    conn.commit()

##query to checkdef login_user(values):
#select * from users where email='gabrielmurunga7@gmail.com';

##function to check email
def check_email(email):
    query="select * from users where email=%s"
    cur.execute(query,(email,))
    
    data=cur.fetchone()
    if data:

       return data

def check_email_pass(email,password):
    query ="select * from users where email=%s and password=%s"
    cur.execute(query,(email,password,))
    data=cur.fetchall()
    return data