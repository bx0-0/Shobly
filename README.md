# Shobly E-commerce Platform

## Project Overview

Shobly is an innovative e-commerce platform that allows users to securely buy, sell, and list products. Developed by a dedicated team of students, it ensures a seamless trading experience. The platform leverages AI for product recommendations and secure transactions.

## Features

- **User Authentication and Profiles**: Users can sign up, log in, and manage their profiles.
- **Product Management**: Users can create, edit, and delete products.
- **Shopping Cart**: Users can add products to their cart.
- **AI-Powered Product Recommendations**: The platform uses AI to predict and recommend products based on user preferences and behavior.
- **Localization**: Supports multiple languages, including Arabic.
- **Transaction Management**: Secure and fast transactions.

## Technology Used

- **Frontend**: User-friendly responsive design.
- **Backend**: Django framework for building the web application.
- **Database**: Django ORM for database interactions.
- **AI**: AI models for product recommendations.

## Models

- **Cart**: Represents the shopping cart with fields for user, product, quantity, and creation date.
- **Product**: Represents the product with fields for title, description, price, images, category, and more.
- **Profile**: Represents the user profile with fields for PayPal email, city, and company name.

## Views

- **create_product**: Handles the creation of new products.
- **product_detail**: Displays detailed information about a product.
- **product_list**: Lists all available products with filtering and pagination.
- **delete_product**: Deletes a product.
- **edit_product**: Edits an existing product.
- **user_products**: Lists products created by the logged-in user.
- **predict**: Handles AI-based product predictions.

## Templates

- **create_product.html**: Form for creating a new product.
- **product_detail.html**: Displays detailed information about a product.
- **product_list.html**: Lists all available products.
- **user_products.html**: Lists products created by the logged-in user.
- **product_prediction.html**: Displays AI-based product predictions.
- **cart.html**: Displays the shopping cart.
- **about_as.html**: Provides information about the project and its features.
- **home.html**: The home page of the application.
- **login.html**: User login form.
- **profile.html**: User profile page.
- **signup.html**: User signup form.

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

- **Predict Products**: Navigate to the product prediction page and use the AI to predict products based on your preferences.

### Localization

- **Language Selection**: The platform supports multiple languages, including Arabic. You can switch languages from the home page.

