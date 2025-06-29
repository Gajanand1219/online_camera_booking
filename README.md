# online camera Booking Website                https://gajanan.pythonanywhere.com/

#
https://github.com/user-attachments/assets/28738b6d-4336-4e57-a966-e655cd751e68

# Online Camera Booking

- **This is an online camera booking website developed using HTML, Bootstrap, CSS, PHP, and JavaScript. It connects to a MySQL database on an XAMPP server, providing a seamless experience for users to browse and rent cameras.**
#
## Features

- **Responsive Design**: Fully responsive layout that works seamlessly on mobile and desktop devices using Bootstrap.
- **Camera Rental Cards**: Dynamic card layout displaying various cameras with images, descriptions, pricing, and rental options.
- **Order Modal**: Users can enter order details (name, mobile number, email, order and return dates, address, and payment method) in a modal that calculates the total cost based on selected rental days.
- **Chat Feature**: An interactive chat interface with basic AI logic to assist users with common inquiries.
- **Contact Form**: Users can submit inquiries, and the section includes contact information and a Google Map embed.

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Bootstrap
- **Backend**: PHP for processing forms and handling user data
- **Database**: MySQL for data storage on XAMPP server

## HTML Structure

### Card Layout for Rentals
- Displays multiple cards for different rental cameras.
- Each card includes:
  - Image of the camera
  - Description
  - Price per day
  - Buttons to add/remove rental days and place an order
- Total cost is dynamically updated based on the selected rental days.

### Order Modal
- Users enter their order details in a modal:
  - Name
  - Mobile Number
  - Email
  - Order and Return Dates
  - Address
  - Payment Method
- Displays total days and cost before submission.

### Contact Section
- Contains a form for users to submit inquiries.
- Displays contact information and links to social media.
- Includes an embedded Google Map for location.

## JavaScript Functionality

### Card Interaction Logic
- Buttons to increase/decrease rental days, updating displayed quantity and total cost.
- The "Order Now" button populates the modal with the selected item's details.

### Chat Feature
- Chat interface for sending messages and receiving predefined responses.
- Basic AI logic for processing user messages.

### Form Submission Handling
- Order, contact, login, and registration forms submitted via AJAX to avoid page reloads.
- Server responses are logged, and forms are reset after submission.
- Modals are animated and managed based on user interactions.

## Installation

1. Clone the repository.
2. Set up XAMPP and create a MySQL database.
3. Import the provided SQL file for the database structure.
4. Configure database connection settings in PHP files.
5. Start the XAMPP server and access the website via a browser.

## Usage

- Browse the camera rental options.
- Use the chat feature for assistance.
- Fill out forms for orders and inquiries.


# Back-end
- backend tables you might use for your online camera booking website, which you can implement in your XAMPP MySQL database:
  ![Screenshot 2024-09-22 234258](https://github.com/user-attachments/assets/a8f6f9fc-e538-4017-95c2-c95a6476640b)
#


### Camera Rental Cards

- Displays multiple cards for different rental cameras. Each card includes:
- **Camera Model 1**
    - Description: This is a great camera for beginners.
    - Price per day: $10
    - Buttons: [Add Day] [Remove Day] [Order Now]
   ![Screenshot 2024-09-22 231602](https://github.com/user-attachments/assets/5ebc5d0a-dd01-419e-b622-7ec322ae2bf0)

  #
  - ![Camera Image 2] **Camera Model 2**
    - Description: Perfect for professional photographers.
    - Price per day: $15
    - Buttons: [Add Day] [Remove Day] [Order Now]
      ![Screenshot 2024-09-22 231621](https://github.com/user-attachments/assets/25d3e7d3-cfe0-44ca-9fcd-0cc0e9f494a1)


#
  - ![Camera Image 3] **Camera Model 3**
    - Description: Compact and easy to carry.
    - Price per day: $8
    - Buttons: [Add Day] [Remove Day] [Order Now]
![Screenshot 2024-09-22 231543](https://github.com/user-attachments/assets/3d47ca55-e5f8-401c-b83b-e2ff17c75fee)

- Total cost is dynamically updated based on the selected rental days.

