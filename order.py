from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_mail import Mail, Message
from datetime import datetime
import mysql.connector
import os
# from openai import OpenAI
from openai import OpenAI

from werkzeug.utils import secure_filename
from fpdf import FPDF
from email.mime.base import MIMEBase
from email import encoders
# from twilio.rest import Client
import time

app = Flask(__name__)
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# Set secret key for sessions
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Make sure this directory exists
app.secret_key = 'your_secret_key'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import mysql.connector as myconn
mydb=myconn.connect(host="localhost",user="root",password="gaju1234?")                    #  CREATE DATABASE WHITH DATA NAME     once create thin commited this code
dbcursor=mydb.cursor()
dbcursor.execute("create database data")

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#  # Setting up SQL database URI
db_host='localhost'
db_user='root'
db_password='gaju1234?'
db_name='data'

#  create table register
# Function to connect to the MySQL database
def get_db_connection():
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return conn

# Create the database table if it doesn't exist

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS register(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    email VARCHAR(30) NOT NULL,
    password VARCHAR(255) NOT NULL,
    number VARCHAR(12) NOT NULL,
    profile_photo VARCHAR(150),
    google_id VARCHAR(50) DEFAULT NULL,  -- Google ID
    facebook_id VARCHAR(50) DEFAULT NULL  -- ✅ New column for Facebook ID
);
''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            number VARCHAR(20),
            email VARCHAR(100),
            order_date DATE,
            return_date DATE,
            address TEXT,
            price_per_day FLOAT,
            total_amount FLOAT,
            total_days int,
            item_name VARCHAR(100),
            payment_method VARCHAR(20),
            user_id INT,
            FOREIGN KEY (user_id) REFERENCES register(id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            rating INT
        )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(25) NOT NULL,
        email VARCHAR(50) NOT NULL,
        rating INT NOT NULL,
        message TEXT NOT NULL
        )
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history(
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_message TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
''')


    conn.commit()
    conn.close()

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Configuring Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'gajanan19022000@gmail.com'  # Your Gmail address
app.config['MAIL_PASSWORD'] = 'zoks tqbh ldkv neqt'  # Your App Password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ✅ Allow HTTP for local testing
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# ✅ Google OAuth Setup
google_bp = make_google_blueprint(
     client_id="513089800096-g2h34cu9k0e0h04culjb3t0okirteqpu.apps.googleusercontent.com",
    client_secret="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",
    scope=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_to="google_login"
)
app.register_blueprint(google_bp, url_prefix="/login")

# ✅ Google Login Route
@app.route("/google")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    user_info = resp.json()

    email = user_info.get("email")
    name = user_info.get("name")
    profile_photo_url = user_info.get("picture")  # Google profile photo URL
    google_id = user_info.get("id")  # Unique Google ID


    if not email:
        flash("Google login failed: No email provided", "error")
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)

    try:
        # ✅ Check if the user exists by email
        cursor.execute("SELECT id, profile_photo FROM register WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            user_id = existing_user[0]
            print("✅ User already exists. Logging in.")
        else:
            # ✅ New user: Insert into `register` table
            cursor.execute("""
                INSERT INTO register (username, email, password, number, profile_photo,google_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, email, "google_auth", "N/A", None, google_id))  # Profile photo will be updated later
            
            conn.commit()
            user_id = cursor.lastrowid  # Get newly inserted user ID
            print("✅ New Google user inserted.")

    except mysql.connector.Error as err:
        print("❌ MySQL Error:", err)
        flash("Database error occurred. Try again later.", "error")
        return redirect("/login")

    finally:
        cursor.close()
        conn.close()

    # ✅ Store user session
    session["user_id"] = user_id

     # Prepare order confirmation email
    subject = "Login Successful"
    message_body = f"""Hello {name},
    Welcome to My DreamShutter Studios! 🎉

    Thank you for signing up with Google. You are now registered and can start exploring our premium photography services.
    
    📸 **Your Registration Details**:
    - Username: {name}
    - ID: {google_id}  ✅ (Your unique identifier)

    You can now book sessions, explore our gallery, and capture your memories with us!
    
    If you have any questions, feel free to reach out:
    📧 **Support:** gajanand1902@gmail.com  
    We look forward to capturing your special moments! 🎊
    
    Best Regards,  
**My Studio Photography Team**  
📍 Visit us:(https://gajanan.pythonanywhere.com/)  

        Thank you 🚀😊!
"""
    msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = message_body
    mail.send(msg)

    return redirect("/")  # Redirect to homepage or profile
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/')
def index():
    return render_template("order1.html")

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username and password match any record in the register table
        cursor.execute("SELECT * FROM register WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()  # Fetch one record
        conn.close()

        if user:  # If a user is found
            session['user_id'] = user[0]  # Store the user ID in session
            return redirect('/')  # Assuming you have a home route
        else:
            flash("User not found. Please register first!", 'error')
            return redirect('/login')

    return render_template("login.html")
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
from flask import Flask, session, jsonify

@app.route('/check_user')
def check_user():
    # Check if user is logged in by checking session
    if 'user_id' in session:  # If user_id exists in session, they are logged in
        return jsonify({'logged_in': True})
    else:
        return jsonify({'logged_in': False})

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        number = request.form['number']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM register WHERE username = %s", (username,))
        existing_user = cursor.fetchone()  # Fetch one result

        if existing_user:
            conn.close()
            return "Username already exists!"

        

        # Insert the new user into the database
        cursor.execute("INSERT INTO register (username, password, email, number) VALUES (%s, %s, %s, %s)",
               (username, password, email, number))

        conn.commit()
        conn.close()


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        # Prepare order confirmation email
        subject = "Registration Successful"
        message_body = f"""Hello {username},
        Welcome to My DreamShutter Studios! 🎉
        
        Thank you for signing up with Google. You are now registered and can start exploring our premium photography services.
        
        📸 **Your Registration Details**:
        - Username: {username}
        - password: {password}  ✅ (Your unique identifier)

        You can now book sessions, explore our gallery, and capture your memories with us!
        
        If you have any questions, feel free to reach out:

        📧 **Support:** gajanand1902@gmail.com  
        We look forward to capturing your special moments! 🎊

        Best Regards,  
        **My Studio Photography Team**  
        📍 Visit us:(https://gajanan.pythonanywhere.com/)  

        Thank you 🚀😊!
        """
        msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[email])
        msg.body = message_body
        mail.send(msg)

#  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////       

        # account_sid = 'AC5bf5d5e5e632a03286ca515e3960c6b7'  # Replace with your Account SID
        # auth_token = '9a2c8136fc6d019c77e6c2a667a3c739'    # Replace with your Auth Token

        # # Create a Twilio client
        # client = Client(account_sid, auth_token)

        # country_code = '+91'
        # formatted_contact = country_code + number

        # # Send an SMS
        # message = client.messages.create(
        #     body=f"""Hello {username},
        # Your registration is successful.Below your registration details:
        #     - Username: {username}
        #     - Password: {password}
        # Use this username and password to login ,and order any products.Thank you!""",

        #     from_='+18589434968',           # Replace with your Twilio phone number
        #     to=formatted_contact              # Recipient's phone number
        # )

        # Redirect to the login page after sending the email
        return redirect('/login')

    return render_template('login.html')
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    # Get the user data from the database using the user_id from the session
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch user details from the 'register' table using the session's user_id
    cursor.execute("SELECT * FROM register WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()

    if user is None:
        return redirect('/login')  # If no user found, redirect to login

    # Fetch user's orders from the 'orders' table
    cursor.execute("SELECT * FROM orders WHERE user_id = %s", (session['user_id'],))
    user_orders = cursor.fetchall()  # Fetch all orders for the user

    conn.close()

    # Map user tuple to field names for easy access in the template
    user_info = {
        'id': user[0],
        'username': user[1],
        'email': user[2],
        'password': user[3],  # Adjust this index if the password field is in a different place
        'number': user[4],
        'profile_photo': user[5]
    }

    # Render the profile page and pass user info and orders to the template
    return render_template('profile.html', user=user_info, orders=user_orders)

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# upload_photo file has an allowed extension
@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    if 'user_id' not in session:
        return redirect('/login')

    if 'file' not in request.files:
        flash("No file uploaded", "error")
        return redirect('/profile')

    file = request.files['file']

    if file.filename == '':
        flash("No selected file", "error")
        return redirect('/profile')

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)  # ✅ Save file in `static/uploads/`

        # ✅ Store the filename (not full path) in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE register SET profile_photo = %s WHERE id = %s", (filename, session['user_id']))
        conn.commit()
        conn.close()

        return redirect('/profile')

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

import stripe

stripe.api_key = "sk_test_51QreFNJRU2FVlSQlyKuQG297bHhNDfspewEbo0p7KQJ3ehfEfK1mMsh05MfokPtl0wPSznQ5ecFrIti7pEou5XjQ00vLewlHRG"

@app.route('/place_order', methods=["POST"])
def place_order():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM register WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    
    if user is None:
        conn.close()
        return redirect('/login')

    name = request.form['name']
    number = request.form['number']
    email = request.form['email']
    order_date_str = request.form['order_date']
    return_date_str = request.form['return_date']
    address = request.form['address']
    payment_method = request.form['payment_method']
    price_per_day = float(request.form['price_per_day'])
    item_name = request.form['item_name']
    order_date = datetime.strptime(order_date_str, '%Y-%m-%d').date()
    return_date = datetime.strptime(return_date_str, '%Y-%m-%d').date()

    total_days = max((return_date - order_date).days, 1)
    total_amount = total_days * price_per_day


    if payment_method == "Cards":
        session['order_data'] = {
            "name": name,
            "number": number,
            "email": email,
            "order_date": order_date_str,
            "return_date": return_date_str,
            "address": address,
            "price_per_day": price_per_day,
            "total_days": total_days,
            "total_amount": total_amount,
            "item_name": item_name,
            "user_id": user[0]
        }
        return redirect(url_for('stripe_payment'))

    cursor.execute('''
        INSERT INTO orders (name, number, email, order_date, return_date, address, price_per_day, total_days, total_amount, item_name, payment_method, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (name, number, email, order_date, return_date, address, price_per_day, total_days, total_amount, item_name, payment_method, user[0]))

    conn.commit()
    conn.close()

    #  Prepare order confirmation email
    from pdf import hi
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id,name, number, item_name, total_amount, order_date, return_date, payment_method, address
        FROM orders
        ORDER BY id DESC LIMIT 1
        """)
    last_order = cursor.fetchone()  # Fetch the last order r

    pdf_file = hi(last_order[0],(session['user_id']) )# Path to the generated PDF file

    subject = "Order Confirmation"
    message_body = f"""Hello {name},

    ORDER SUCCESSFUL

    Thank you for your order! Your order is being processed and will be on its way to you soon. Here's a summary of your order:

    If you have any questions or need help, you can reply to this email or reach out to our customer support.

    Happy shopping! 😊😊
    """

    # Read the PDF content
    with open(pdf_file, "rb") as attachment:
        pdf_content = attachment.read()

    # Create the email message
    msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = message_body

    # Attach the PDF file to the email
    msg.attach(filename="order_invoice.pdf", content_type="application/pdf", data=pdf_content)

    # Send the email
    mail.send(msg)

    return """
    <script>
        alert("Order Successful! Your order has been placed. Check your email for details.");
        window.location.href = "/";
    </script>
    """


@app.route('/stripe_payment')
def stripe_payment():
    order_data = session.get('order_data')

    if not order_data:
        return redirect('/')

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {'name': order_data["item_name"]},
                'unit_amount': int(order_data["total_amount"] * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('payment_success', _external=True),
        cancel_url=url_for('payment_cancel', _external=True),
    )

    return redirect(checkout_session.url)
@app.route('/payment_success')
def payment_success():
    order_data = session.pop('order_data', None)

    if not order_data:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO orders (name, number, email, order_date, return_date, address, price_per_day, total_days, total_amount, item_name, payment_method, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        order_data["name"], order_data["number"], order_data["email"],
        order_data["order_date"], order_data["return_date"], order_data["address"],
        order_data["price_per_day"], order_data["total_days"], order_data["total_amount"],
        order_data["item_name"], "Cards", order_data["user_id"]
    ))

    conn.commit()
    conn.close()
    #  Prepare order confirmation email
    from pdf import hi
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id,name, number, item_name, total_amount, order_date, return_date, payment_method, address
        FROM orders
        ORDER BY id DESC LIMIT 1
        """)
    last_order = cursor.fetchone()  # Fetch the last order r

    pdf_file = hi(last_order[0],(session['user_id']) )# Path to the generated PDF file

    subject = "Order Confirmation"
    message_body = f"""Hello {order_data["name"]},

    ORDER SUCCESSFUL

    Thank you for your order! Your order is being processed and will be on its way to you soon. Here's a summary of your order:

    If you have any questions or need help, you can reply to this email or reach out to our customer support.

    Happy shopping! 😊😊
    """

    # Read the PDF content
    with open(pdf_file, "rb") as attachment:
        pdf_content = attachment.read()

    # Create the email message
    msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[ order_data["email"]])
    msg.body = message_body

    # Attach the PDF file to the email
    msg.attach(filename="order_invoice.pdf", content_type="application/pdf", data=pdf_content)

    # Send the email
    mail.send(msg)

    return """
    <script>
        alert("Payment Successful! Your order has been placed. Check your email for details.");
        window.location.href = "/";
    </script>
    """

@app.route('/payment_cancel')
def payment_cancel():
    return """
    <script>
        alert("Order Cancelled. Please try again.");
        window.location.href = "/";
    </script>
    """

# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route('/send_contact', methods=["POST"])
def send_email():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    phone = request.form['phone']
    # Create email message
    msg = Message(subject=f"New Contact Messge from {name}: {subject}",  # Include name in subject
                  sender=app.config['MAIL_USERNAME'],             # Must be your verified sender email
                  recipients=['gajanan19022000@gmail.com'])        # Use your email as recipient
                  
    # Include user details in the body of the email
    msg.body = f"Message from :- {name}\n\n Email:-{email}\n\Requirment:-{subject}\n\nmessage:-{message}\n\nNumber:-{phone}"

    # Optionally set the reply-to header to the user's email
    msg.reply_to = email

    mail.send(msg)
    return redirect('/')


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/blog')
def blog():
    
    return render_template("blog.html")

# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/garelly')
def garelly():
    
    return render_template("garelly.html")

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route("/contact", methods=["GET"])
def contact():
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve all ratings from the database
    cursor.execute("SELECT * FROM ratings")
    ratings = cursor.fetchall()

    # Retrieve all feedback from the database
    cursor.execute("SELECT * FROM feedback")
    feedback = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Pass ratings to the template (even if empty)
    return render_template('contact.html', ratings=ratings , feedback=feedback)
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@app.route("/rating", methods=["POST"])
def rating():
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get form data
    username = request.form['username']
    rating = request.form['rating']

    # Insert rating into the database
    cursor.execute("INSERT INTO ratings (username, rating) VALUES (%s, %s)", (username, rating))
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    # Redirect to /contact to display all ratings
    return redirect(url_for('contact'))
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Feedback submission route
@app.route("/feedback", methods=["POST"])
def submit_feedback():
    if request.method == "POST":
        username = request.form["name"]
        email = request.form["email"]
        rating = request.form["rating"]
        message = request.form["message"]

        # Save feedback to MySQL database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO feedback (username, email, rating, message) VALUES (%s, %s, %s, %s)", 
                       (username, email, rating, message))
        conn.commit()
        conn.close()

        return redirect(url_for("contact"))
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/blogs/<blog_id>')
def get_blog(blog_id):
    # Renders the combined blogs file and passes the blog_id
    return render_template('blogs.html', blog_id=blog_id)
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

client = OpenAI(api_key="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")

# Route to save user message & AI response
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    try:
        # Get AI response
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
        ai_response = completion.choices[0].message.content

        # Save to MySQL
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO chat_history (user_message, ai_response) VALUES (%s, %s)"
        cursor.execute(query, (user_message, ai_response))
        conn.commit()

        return jsonify({"response": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
 # Route to fetch chat history
@app.route("/chat", methods=["GET"])
def get_chat_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, ai_response, timestamp FROM chat_history ORDER BY timestamp ASC")
    chat_data = cursor.fetchall()

    # Return data with each message in a separate block
    chat_list = [
        {
            "ai_input": row[0],
            "ai_responce": row[1],
            "time": row[2].strftime("%Y-%m-%d %H:%M:%S")
        } for row in chat_data
    ]

    return jsonify(chat_list)


# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    create_table()
    app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000, threaded=True)



# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
