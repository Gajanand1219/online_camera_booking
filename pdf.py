from fpdf import FPDF
import mysql.connector

# Database Configuration
db_host = 'localhost'
db_user = 'root'
db_password = 'gaju1234?'
db_name = 'data'

def get_db_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

def hi(order_id, user_id):
    class PDFInvoice(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 16)  # Use default core font
            self.cell(0, 10, 'Order Confirmation', align='C', ln=1)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 10)  # Use default core font
            self.cell(0, 10, 'Thank you for shopping with us!', align='C')

    # Create instance of FPDF
    pdf = PDFInvoice()
    # Add a page
    pdf.add_page()

    # Set font
    pdf.set_font('Arial', '', 12)

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch user data from register table based on the user_id
        cursor.execute("""
            SELECT id, username, email, number FROM register WHERE id = %s
        """, (user_id,))  # Ensure user_id is a single value passed as tuple
        user = cursor.fetchone()  # Fetch user details
        
        if user:
            # Add content for user details
            pdf.cell(0, 10, f"Hello {user[1]}", ln=1)  # username from the register table
            pdf.ln(5)

            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, "User Description.")
            pdf.ln(8)
            pdf.cell(5, 5, 'ORDER SUCCESSFUL', ln=3)
            pdf.ln(5)
            pdf.multi_cell(0, 5, """Thank you for your order!
        Your order is being processed and will be on its way to you soon. Here's a summary of your order:""")


            # Create Table for user details
            user_details = [
                ("User ID", str(user[0])),  # id
                ("Username", user[1]),      # username
                ("Email", user[2]),         # email
                ("Phone", user[3]),         # phone
            ]
            
            # Table headers for user details
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(95, 10, 'Description', border=1, align='C')
            pdf.cell(95, 10, 'Details', border=1, align='C')
            pdf.ln()

            # Table content for user details
            pdf.set_font('Arial', '', 12)
            for key, value in user_details:
                pdf.cell(95, 10, key, border=1)
                pdf.cell(95, 10, str(value), border=1)
                pdf.ln()

            pdf.ln(5)  # Add a line break
        else:
            pdf.multi_cell(0, 10, "No user details found for this user.")
            pdf.ln(10)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

    # Fetch the last order details using the order_id
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, item_name, total_amount, order_date, return_date, payment_method, address
            FROM orders
            WHERE id = %s
        """, (order_id,))
        last_order = cursor.fetchone()  # Fetch the last order row

        if last_order:
            # Create Table for order details
            order_details = [
                ("Order Id", str(last_order[0])),  # id
                ("Item Name", last_order[1]),      # item_name
                ("Total Amount", f"${last_order[2]:.2f}"),  # total_amount
                ("Order Date", last_order[3].strftime('%Y-%m-%d')),  # order_date
                ("Return Date", last_order[4].strftime('%Y-%m-%d')),  # return_date
                ("Payment Method", last_order[5]),  # payment_method
                ("Address", last_order[6]),         # address
            ]
            pdf.set_font('Arial', 'B', 12)
            pdf.multi_cell(0, 5, " Oredr Description.")
            pdf.ln(10)
            # Table headers for order details
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(95, 10, 'Description', border=1, align='C')
            pdf.cell(95, 10, 'Details', border=1, align='C')
            pdf.ln()

            # Table content for order details
            pdf.set_font('Arial', '', 12)
            for key, value in order_details:
                pdf.cell(95, 10, key, border=1)
                pdf.cell(95, 10, str(value), border=1)
                pdf.ln()

        else:
            pdf.multi_cell(0, 10, "No order details found for this user.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

    pdf.ln(10)
    pdf.multi_cell(0, 10, """If you have any questions or need help, you can reply to this email or reach out to our customer support.
    Happy shopping!""")

    # Save the PDF
    file_name = f"invoice.pdf"
    pdf.output(file_name)

    # print(f"PDF Invoice for Order ID {order_id} generated successfully!")
    return file_name


# Example usage: call the function with an order_id
# Replace with the actual order_id to generate the invoice
# hi(1)
