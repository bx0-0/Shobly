# Shobly E-commerce Platform

## Project Overview
Shobly is an innovative e-commerce platform that allows users to securely buy, sell, and list products.

## Features
- **User Authentication and Profiles**: Users can sign up, log in, and manage their profiles.
- **Product Management**: Users can create, edit, and delete products.
- **Shopping Cart**: Users can add products to their cart.
- **AI-Powered Product Recommendations**: The platform uses similarity algorithms to recommend products based on user descriptions.
- **Localization**: Supports multiple languages, including Arabic.
- **Transaction Management**: Secure and fast transactions.
- **Shipping Simulation**: Simulates a shipping company to track and manage product shipments.

## Technology Used
- **Frontend**: User-friendly responsive design.
- **Backend**: Django framework for building the web application.
- **Database**: Django ORM for database interactions.
- **AI**: Similarity-based algorithms for product recommendations.
- **Shipping Simulation**: Custom script to simulate shipping company operations.

## Models
- **Cart**: Represents the shopping cart with fields for user, product, quantity, and creation date.
- **Product**: Represents the product with fields for title, description, price, images, category, and more.
- **Profile**: Represents the user profile with fields for PayPal email, city, and company name.
- **Shipping**: Represents the shipping details with fields for tracking ID, status, and delivery date.

## Views
- **create_product**: Handles the creation of new products.
- **product_detail**: Displays detailed information about a product.
- **product_list**: Lists all available products with filtering and pagination.
- **delete_product**: Deletes a product.
- **edit_product**: Edits an existing product.
- **user_products**: Lists products created by the logged-in user.
- **recommend_products**: Handles AI-based product recommendations.
- **shipping_status**: Displays the shipping status of a product.

## Templates
- **create_product.html**: Form for creating a new product.
- **product_detail.html**: Displays detailed information about a product.
- **product_list.html**: Lists all available products.
- **user_products.html**: Lists products created by the logged-in user.
- **product_recommendations.html**: Displays AI-based product recommendations.
- **cart.html**: Displays the shopping cart.
- **about_as.html**: Provides information about the project and its features.
- **home.html**: The home page of the application.
- **login.html**: User login form.
- **profile.html**: User profile page.
- **signup.html**: User signup form.
- **shipping_status.html**: Displays the shipping status of a product.

## Translation Files
- **django.po**: Contains translations for various strings used in the application, supporting multiple languages including Arabic.

## Installation
### Prerequisites
- Python 3.8+
- Django 3.2+
- Virtualenv (optional but recommended)

### Steps
1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/shobly.git
   cd shobly
   ```
2. **Create a virtual environment (optional but recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Apply migrations**
   ```sh
   python manage.py migrate
   ```
5. **Create a superuser**
   ```sh
   python manage.py createsuperuser
   ```
6. **Run the development server**
   ```sh
   python manage.py runserver
   ```
7. **Access the application**
   Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage
### User Authentication
- **Sign Up**: Navigate to the signup page and fill in the required details.
- **Login**: Navigate to the login page and enter your credentials.
- **Profile**: Manage your profile by updating your details.

### Product Management
- **Create Product**: Navigate to the create product page and fill in the product details.
- **Edit Product**: Navigate to the product detail page and click on the edit button.
- **Delete Product**: Navigate to the product detail page and click on the delete button.
- **List Products**: Navigate to the product list page to view all available products.

### Shopping Cart
- **Add to Cart**: Navigate to the product detail page and click on the add to cart button.
- **View Cart**: Navigate to the cart page to view the items in your cart.

### AI-Powered Product Recommendations
- **Recommend Products**: Enter a product description, and the platform will recommend similar products using similarity algorithms.

### Localization
- **Language Selection**: The platform supports multiple languages, including Arabic. You can switch languages from the home page.

### Transaction Management
- **Secure Transactions**: The platform ensures secure and fast transactions.

### Shipping Simulation
- **Shipping Status**: The platform includes a script to simulate a shipping company. This script allows users to track the status of their shipments. The script is essential for providing real-time updates on the shipping process, ensuring transparency and reliability for both buyers and sellers.

#### Benefits of Shipping Simulation
1. **Real-Time Tracking**: Users can track the status of their shipments in real-time, providing transparency and reliability.
2. **Efficiency**: The script automates the shipping process, reducing manual effort and potential errors.
3. **Customer Satisfaction**: Real-time updates and transparency enhance customer satisfaction and trust.
4. **Data Management**: The script helps in managing shipping data efficiently, making it easier to analyze and improve the shipping process.

#### How to Use the Shipping Simulation Script
1. **Install the Script**: Ensure the shipping simulation script is installed and configured correctly.
2. **Run the Script**: Execute the script to start simulating the shipping company operations.
3. **Track Shipments**: Use the platform to track the status of your shipments in real-time.

## AI-Powered Product Recommendations
The AI-powered recommendation system uses similarity algorithms to match user-provided descriptions with the most relevant products in the database. It does not rely on machine learning models but instead leverages techniques like:
- **Cosine Similarity**: To measure the similarity between product descriptions.
- **TF-IDF (Term Frequency-Inverse Document Frequency)**: To weigh the importance of words in product descriptions.
- **Keyword Matching**: To identify key terms in user input and match them with product attributes.

### Example Workflow
1. **User Input**: A user enters a description such as "I'm looking for a lightweight laptop with long battery life."
2. **Processing**: The system processes the input using TF-IDF and cosine similarity to compare it with product descriptions in the database.
3. **Output**: The system returns a list of products that closely match the description, such as laptops with specifications matching "lightweight" and "long battery life."

This approach ensures that users receive accurate and relevant product recommendations without the complexity of training machine learning models.

## Shipping Simulation Script
The shipping simulation script is implemented in the `simulate_shipping_company.py` file. Below is an explanation of the key functions and their purposes:

### Functions
1. **home()**
   - **Purpose**: Returns a JSON response indicating that the shipping company simulation is active.
   - **Usage**: This function is used to verify that the shipping simulation script is running.
   ```python
   def home():
       return jsonify("Shipping Company Simulation")
   ```

2. **simulate_shipping_company()**
   - **Purpose**: Simulates a successful shipping process.
   - **Parameters**:
     - `data`: JSON data containing order details, buyer email, and seller email.
     - `auth_header`: Authorization header for API authentication.
   - **Usage**: This function is called when an order is successfully shipped. It returns a JSON response with the shipping status and order details.
   ```python
   def simulate_shipping_company():
       data = request.json
       order_details = data["product_details"]
       buyer_email = data["buyer_email"]
       seller_email = data["seller_email"]
       auth_header = request.headers.get("Authorization")
       if auth_header != "1234567890abcdef":
           return jsonify({"error": "Unauthorized"}), 401
       shipping_response = (
           f"Order {order_details['order_number']} has been shipped successfully"
       )
       respon = {
           "shipping_response": shipping_response,
           "order_details": order_details,
           "status": "Shipped",
       }
       return jsonify(respon), 200
   ```

3. **simulate_failed_shipping_company()**
   - **Purpose**: Simulates a failed shipping process.
   - **Parameters**:
     - `data`: JSON data containing order details, buyer email, and seller email.
     - `auth_header`: Authorization header for API authentication.
   - **Usage**: This function is called when an order fails to be shipped. It returns a JSON response with the shipping status and order details.
   ```python
   def simulate_failed_shipping_company():
       data = request.json
       order_details = data["product_details"]
       buyer_email = data["buyer_email"]
       seller_email = data["seller_email"]
       auth_header = request.headers.get("Authorization")
       if auth_header != "1234567890abcdef":
           return jsonify({"error": "Unauthorized"}), 401
       shipping_response = (
           f"Order {order_details['order_number']} has failed to be shipped"
       )
       respon = {
           "shipping_response": shipping_response,
           "order_details": order_details,
           "status": "Failed",
       }
       return jsonify(respon), 200
   ```

### Script Usage
To use the shipping simulation script, follow these steps:
1. **Ensure the script is installed and configured correctly**.
2. **Run the script** to start simulating the shipping company operations.
3. **Track shipments** using the platform to view real-time updates on the shipping status.
