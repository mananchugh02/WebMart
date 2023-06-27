import mysql.connector as sql
import random

connection = sql.connect(host="localhost", user="root", password="1234", database="WebMart")
current_user= None
current_admin= None
current_delivery_agent= None


def user_Signup(name, gender, age, address, phone_number, password):
    cursor = connection.cursor()
    query = "INSERT INTO customer (Name, Gender, Age, Address, PhoneNumber, Password) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(name, gender, age, address, phone_number, password)
    cursor.execute(query)
    connection.commit()
    cursor.close()


def user_Login(name, password):
    global current_user
    try:
        cursor = connection.cursor()
        cursor.execute("select user_id, name from customer where name = '{}' and password = '{}'".format(name, password))
        data = cursor.fetchall()
        [id,  name] = data[0]
        current_user = id
        print("Successfully Logged In as {} (USER ID: '{}')".format(name,id))
        cursor.close()
        return True
    except:
        print("Incorrect username or password. Please try again.")
        return False
    


def admin_Signup(name, gender, age, username, password):
    
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Admins (Name, Gender, Age, Username, Password) VALUES ('{}', '{}', '{}', '{}', '{}')".format(name, gender, age, username, password))
    connection.commit()
    cursor.close()


def admin_Login(username, password):

    global current_admin
    try:
        cursor = connection.cursor()
        cursor.execute("select admin_id, name from Admins where username = '{}' and password = '{}'".format(username, password))
        data = cursor.fetchall()
        [id,  name] = data[0]
        current_admin = id
        print("Succesfully Loged In as {} (Admin ID: '{}')".format(name,id))
        cursor.close()
        return True

    except:
        print("Incorrect username or password. Please try again.")
        return False
    


def delivery_Agent_Signup(name, gender, age, phone_number, password):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO DeliveryAgent (Name, Gender, Age, PhoneNumber, Rating, Password) VALUES ('{}', '{}', '{}', '{}', {}, '{}')".format(name, gender, age, phone_number, 0, password))
    connection.commit()
    cursor.close()


def delivery_Agent_Login(name, password):
    global current_delivery_agent
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DeliveryAgent_ID, Name FROM DeliveryAgent WHERE Name = '{}' AND Password = '{}'".format(name, password))
        data = cursor.fetchall()
        [id, name] = data[0]
        current_delivery_agent = id
        print("Successfully logged in as {} (Delivery Agent ID: '{}')".format(name, id))
        cursor.close()
        return True

    except:
        print("Incorrect username or password. Please try again.")
        return False


def add_category(name, discount, description):

    cursor = connection.cursor()
    cursor.execute("insert into category values ('{}','{}','{}','{}')".format(name, discount, description, current_admin))
    cursor.commit()
    cursor.close()


def delete_category(name):
    try:
        cursor = connection.cursor
        cursor.execute("DELETE FROM Category WHERE Name = '{}' ".format(name))
        cursor.commit()
        cursor.close()
        print("Succesfully deleted")
    except Exception as e:
        print("There was an error in deleting the category")
        print(e)


def add_product(name, price, quantity, discount, description, img, c_id, retailer_id):
    try:
        cursor = connection.cursor()
        query = "INSERT INTO Product (Name, Price, Quantity, Discount, Description, Image, Category_ID, Retailer_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (name, price, quantity, discount, description, img, c_id, retailer_id)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        print("\nSuccessfully added product")
    except Exception as e:
        print("There was an error in adding the product")
        print(e)


def delete_product(name):
    try:
        cursor = connection.cursor
        cursor.execute("DELETE FROM Product WHERE Name = '{}' ".format(name))
        cursor.commit()
        cursor.close()
        print("Succesfully deleted")
    except Exception as e:
        print("There was an error in deleting the product")
        print(e)


def add_discount_product(name, discount):
    try:
        cursor = connection.cursor()
        query = "UPDATE Product SET Discount = %s WHERE Name = %s"
        values = (discount, name)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        print("Successfully updated product discount")
    except Exception as e:
        print("There was an error in updating the product discount")
        print(e)



def view_cart():
    global current_user
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Cart.Cart_ID, Product.Name AS ProductName, Cart.Quantity, (Product.Price * Cart.Quantity) AS TotalPrice FROM Cart INNER JOIN Product ON Cart.Product_ID = Product.Product_ID WHERE Cart.User_ID = %s AND Cart.Status = 0;", (current_user,))
        cart_data = cursor.fetchall()
        if cart_data:
            print("\nCurrent Cart Items:")
            print("--------------------")
            for item in cart_data:
                print(f"Cart ID: {item[0]}, Product Name: {item[1]}, Quantity: {item[2]}, Price: {item[3]}")
        else:
            print("\nYour cart is empty!")
    except Exception as e:
        print(e)


def view_order_using_view():
    global current_user
    try:
        cursor = connection.cursor()
        query = "CREATE VIEW OrderDetails AS SELECT Orders.Order_ID, Orders.Order_Amount, Orders.Cart_ID, Customer.Name AS CustomerName, Product.Name AS ProductName, DeliveryAgent.Name AS DeliveryAgentName FROM Orders JOIN Customer ON Orders.User_ID = Customer.User_ID JOIN Cart ON Orders.Cart_ID = Cart.Cart_ID JOIN Product ON Cart.Product_ID = Product.Product_ID JOIN DeliveryAgent ON Orders.DeliveryAgent_ID = DeliveryAgent.DeliveryAgent_ID;"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("Successfully updated product discount")
    except Exception as e:
        print(e)



def view_all_products():
    global current_user
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Category.Name AS CategoryName, Product.Product_ID, Product.Name AS ProductName, Product.Price, Product.Quantity FROM Category INNER JOIN Product ON Category.Category_ID = Product.Category_ID ORDER BY CategoryName;")
        data = cursor.fetchall()
        print(data)
    except Exception as e:
        print(e)


def add_products(p_id, quantity):
    global current_user
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Cart (User_ID, Product_ID, Quantity) VALUES (%s, %s, %s)", (current_user, p_id, quantity))
        connection.commit()
        cursor = connection.cursor()
        cursor.execute("UPDATE Product SET Quantity = Quantity - %s WHERE Product_ID = %s", (quantity, p_id))
        connection.commit()
        print("\nProduct added to cart successfully!")
    except Exception as e:
        print(e)


def print_orders_del():
    global current_user
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Orders WHERE DeliveryAgent_ID = 1")
        data = cursor.fetchall()
        print(data)
    except Exception as e:
        print(e)


def checkout_cart():
    global current_user
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Cart.Cart_ID, Product.Name AS ProductName, Cart.Quantity, (Product.Price * Cart.Quantity) AS TotalPrice FROM Cart INNER JOIN Product ON Cart.Product_ID = Product.Product_ID WHERE Cart.User_ID = %s AND Cart.Status = 0;", (current_user,))
        cart_data = cursor.fetchall()
        if cart_data:
            print("\nCurrent Cart Items:")
            print("--------------------")
            for item in cart_data:
                print(f"\nCart ID: {item[0]}, Product Name: {item[1]}, Quantity: {item[2]}, Price: {item[3]}\n")
        else:
            print("\nYour cart is empty!")

        c_id = input("Enter the ID of cart you want to order: ")
        response = input("Are you sure you want to continue (y/n): " )
        if(response == 'n'):
            return
        elif(response == 'y'):
            delivery_agent_id = random.randint(1, 3)
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Orders (User_ID, DeliveryAgent_ID, Order_Amount, Order_Date, Cart_ID) SELECT c.User_ID, %s, c.Quantity * p.Price, CURDATE(), c.Cart_ID FROM Cart c JOIN Product p ON c.Product_ID = p.Product_ID WHERE c.Cart_ID = %s;", (delivery_agent_id, c_id, ))
            connection.commit()
            cursor = connection.cursor()
            cursor.execute(" UPDATE Cart SET status = 1 WHERE Cart_ID = %s;", (c_id, ))
            connection.commit()
            cursor = connection.cursor()
            cursor.execute(" UPDATE DeliveryAgent SET Availibility = 0 WHERE DeliveryAgent_ID = %s;", (delivery_agent_id, ))
            connection.commit()
            print("Order Placed succesfully!")
        else:
            print("Wrong Prompt :(")
            return
    except Exception as e:
        print(e)



def top_three_categories(): # OLAP QUERY
#   Top 3 categoires that were added most in the cart
#   This is an OLAP query because it uses the aggregation function SUM() to aggregate the total amount spent by each customer, and GROUP BY to group the results by the Customer.User_ID column. The ORDER BY clause sorts the results in descending order of the total amount spent, and the LIMIT clause returns only the top 3 customers.

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT c.Name AS Category_Name, SUM(c2.Quantity) AS Total_Quantity FROM Category c JOIN Product p ON p.Category_ID = c.Category_ID JOIN Cart c2 ON c2.Product_ID = p.Product_ID GROUP BY c.Category_ID ORDER BY Total_Quantity DESC LIMIT 3;")
        data = cursor.fetchall()
        print(data)
    except Exception as e:
        print(e)


def total_sales_by_retailers(): # OLAP QUERY
# Total sales made by each retailer for the current month.
#We need to join the Orders table with the Product table to get the details of the products sold in the current month.
# Next, we need to join the Product table with the Retailer table to get the details of the retailer who sold the products.
# We need to group the results by the retailer's name and calculate the total sales made by each retailer in the current month.

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT R.Name as RetailerName, SUM(O.Order_Amount) as TotalSales FROM Orders O JOIN Cart C ON O.Cart_ID = C.Cart_ID JOIN Product P ON C.Product_ID = P.Product_ID JOIN Retailer R ON P.Retailer_ID = R.Retailer_ID WHERE MONTH(O.Order_Date) = MONTH(CURRENT_DATE()) AND YEAR(O.Order_Date) = YEAR(CURRENT_DATE()) GROUP BY R.Retailer_ID;")
        data = cursor.fetchall()
        print(data)
    except Exception as e:
        print(e)


def total_sales_by_each_category_and_retialer(): #OLAP QUERY
#Total Sales made by categoyr and retailer

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Category.Name AS Category, Retailer.Name AS Retailer, SUM(Orders.Order_Amount) AS TotalSales FROM Orders INNER JOIN Cart ON Orders.Cart_ID = Cart.Cart_ID INNER JOIN Product ON Cart.Product_ID = Product.Product_ID INNER JOIN Category ON Product.Category_ID = Category.Category_ID INNER JOIN Retailer ON Product.Retailer_ID = Retailer.Retailer_ID GROUP BY Category.Category_ID, Retailer.Retailer_ID")
        data = cursor.fetchall()
        print(data)
    except Exception as e:
        print(e)


def top_five_products(): #OLAP QUERY
# Top 5 products Sold

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT Product.Name, SUM(Orders.Order_Amount) as Total_Sales FROM Orders INNER JOIN Cart ON Orders.Cart_ID = Cart.Cart_ID INNER JOIN Product ON Cart.Product_ID = Product.Product_ID GROUP BY Product.Name WITH ROLLUP HAVING Product.Name IS NOT NULL ORDER BY Total_Sales DESC LIMIT 5;")
        data = cursor.fetchall()
        print(data)
    except Exception as e:
        print(e)


while(True):
    choice = input("Please Choose one of the following options: \n\n1.) User Prompt \n2.) Admin Propmt\n3.) Delivery Agent Prompt\n4.) Exit\n‣ ")
    if choice == '1':
        print("\nWelcome, User!")

        while True:
            choice1 = input("\n\nPlease choose one of the following options: \n1. Sign up\n2. Login\n3. Back\n‣ ")

            if choice1 == '1':
                print("Please enter your following Details: \n")

                name = input("\nFull Name: ")
                gender = input("Gender (Male/Female/Other): ")
                age = int(input("Age: "))
                address = input("Address: ")
                phone_number = input("Phone Number: ")
                password = input("Password: ")

                user_Signup(name, gender, age, address, phone_number, password)
                print("Succesfully Registerd !!.")


            elif choice1 == '2':

                username = input("\nName: ")
                password = input("Password: ")
                is_authenticated = user_Login(username, password)

                if is_authenticated:

                    while is_authenticated:
                        choice4 = input("\n\nPlease choose one of the following options: \n1. View All Products\n2. View Cart\n3. Add Items Into Cart\n4. Checkout Cart\n5. Logout\n‣ ")
                        if choice4 == '1':
                            view_all_products()

                        elif choice4 == '2':
                            view_cart()

                        elif choice4 == '3':
                            p_id = input("Enter the ID of the product you want to add: ")
                            quantity = input("Enter the quantity of the product you want: ")
                            add_products(p_id, quantity)

                        elif choice4 == '4':
                            checkout_cart()

                        elif choice4 == '5':
                            current_user = None
                            print("Successfully logged Out")
                            break

            elif choice1 == '3':
                break

            else:
                print("Invalid choice. Please try again.")

    elif choice == "2":
        print("\nWelcome, Admin!")

        while True:
            choice2 = int(input("\n\nPlease choose one of the following options: \n1. Sign up\n2. Login\n3. Back\n‣ "))

            if choice2 == 1:
                print("Please enter your following Details: \n")

                name = input("\nFull Name: ")
                gender = input("Gender (Male/Female/Other): ")
                age = int(input("Age: "))
                UserName = input("UserName: ")
                password = input("Password: ")
                admin_Signup(name, gender, age, UserName, password)
                print("Succesfully Registerd !!.")
                

            elif choice2 == 2:

                username = input("\nUserName: ")
                password = input("Password: ")
                is_authenticated = admin_Login(username, password)

                if is_authenticated:

                    while is_authenticated:
                        choice4 = input("\n\nPlease choose one of the following options: \n1. Add Category\n2. Delete Category\n3. Add Product\n4. Delete Product\n5. Add Discount\n6. Top 3 categories\n7. Total Sales by Retailers\n8. Perfomance of each category \n9.Top 5 Products \n10. Log Out\n‣ ")
                        if choice4 == '1':

                            name = input("Name: ")
                            discount = input("Discount: ")
                            description = input("Description: ")
                            add_category(name,discount,description)


                        elif choice4 == '2':

                            name = input("Please enter the name of the category you want to delete: ")
                            delete_category(name)
                            pass

                        elif choice4 == '3':

                            name = input("Name: ")
                            price = input("Price:  ")
                            quantity =  input("Stock quantity: ")
                            discount = input("Discount:  ")
                            description = input("Description: ")
                            img = input("Enter the sample image link: ")
                            c_id = input("Category ID: ")
                            retailer_id = input("Retailer ID: ")
                            add_product(name, price, quantity, discount, description, img, c_id, retailer_id)

                        elif choice4 == '4':
                            name = input("Please enter the name of the product you want to delete: ")
                            delete_product(name)

                        elif choice4 == '5':
                            name = input("Please enter the name of the product in which you want to add discount: ")
                            discount = input("Enter the discount: ")
                            add_discount_product(name, discount)

                        elif choice4 == '6':
                            top_three_categories()
                        
                        elif choice4 == '7':
                            total_sales_by_retailers()
                        
                        elif choice4 == '8':
                            total_sales_by_each_category_and_retialer()

                        elif choice4 == '9':
                            top_five_products()

                        elif choice4 == '10':
                            current_admin = None
                            print("Succesfully Logged Out.")
                            break
                        else:
                            print("Please choose a valid option.")

            elif choice2 == 3:
                break
            else:
                print("Invalid choice. Please try again.")

    elif choice == "3":
        print("\n\nWelcome, Delievery Agent !")

        while True:
            choice3 = int(input("\n\nPlease choose one of the following options: \n1. Sign up\n2. Login\n3. Back\n‣ "))

            if choice3 == 1:
                print("Please enter your following Details: \n")

                name = input("\nFull Name: ")
                gender = input("Gender (Male/Female/Other): ")
                age = int(input("Age: "))
                phone_number = input("Phone Number: ")
                password = input("Password: ")
                print("\nDear Delivery Agent, initially your rating would be set to 0.")
                delivery_Agent_Signup(name, gender, age, address, phone_number, password)
                print("Succesfully Registerd !!.")
                

            elif choice3 == 2:

                username = input("\nUsername: ")
                password = input("Password: ")
                is_authenticated = delivery_Agent_Login(username, password)
    
                if is_authenticated:
                    print("1) Show all orders")
                    input8 = int(input("Enter your choice"))
                    if(input8 == 1):
                        print_orders_del()

            elif choice3 == 3:
                break
            else:
                print("Invalid choice. Please try again.")


    elif choice == "4":
        break

    else:
        print("\nPlease select one of the given choices")


