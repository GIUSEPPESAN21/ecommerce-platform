[README.md](https://github.com/user-attachments/files/23570727/README.md)
# E-Commerce Platform

A professional e-commerce platform built with Streamlit, Firebase, and Python. Inspired by MercadoLibre, Amazon, and Temu.

## Features

- 🛒 Product catalog with search and filtering
- 🛍️ Shopping cart management
- 💳 Secure checkout process
- 👤 User authentication and accounts
- 📦 Order management
- 🔍 Advanced product search
- 📱 Responsive design

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** Firebase Firestore
- **Authentication:** Firebase Auth
- **Storage:** Firebase Storage
- **Hosting:** Streamlit Cloud

## Prerequisites

- Python 3.8+
- Firebase project with Firestore, Authentication, and Storage enabled
- Google Cloud account (for Firebase)
- Streamlit Cloud account (for deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/GIUSEPPESAN21/New-Software.git
cd New-Software
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Firebase Setup

1. Create a Firebase project at https://console.firebase.google.com/

2. Enable the following services:
   - Firestore Database
   - Authentication
   - Storage

3. Generate a service account key:
   - Go to Firebase Console → Project Settings → Service Accounts
   - Click "Generate New Private Key"
   - Save the JSON file (DO NOT commit it to Git)

4. Get your Firebase Web API Key (required for authentication):
   - Go to Firebase Console → Project Settings → General
   - Scroll down to "Your apps" section
   - If you don't have a web app, click "Add app" and select Web (</>) icon
   - Copy the "Web API Key" (also called "API Key" or "Browser Key")
   - This key is safe to use in client-side applications

### Streamlit Cloud Deployment

1. Push your code to GitHub

2. Connect your repository to Streamlit Cloud:
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository

3. Configure secrets in Streamlit Cloud:
   - Go to your app settings
   - Click "Secrets"
   - Add the following secrets:

```toml
# Firebase Credentials (from your service account JSON)
[firebase_credentials]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR-KEY\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."

# Firebase Web API Key (required for authentication)
firebase_api_key = "your-firebase-web-api-key"

# Gemini API Key (optional)
[gemini]
api_key = "your-gemini-api-key"
# OR use this format:
GEMINI_API_KEY = "your-gemini-api-key"
```

### Local Development

1. Create `.streamlit/secrets.toml` file:
```bash
mkdir -p .streamlit
```

2. Copy your Firebase service account JSON content to `.streamlit/secrets.toml` in the format shown above

3. Run the application:
```bash
streamlit run app.py
```

## Project Structure

```
/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore file
├── README.md                  # This file
├── firebase_config.py         # Firebase configuration (legacy - preserved)
├── gemini_client.py           # Gemini client (legacy - preserved)
├── components/                # UI components
│   ├── __init__.py
│   ├── auth.py                # Authentication components
│   ├── product_card.py        # Product card component
│   ├── product_list.py        # Product list component
│   ├── cart_summary.py        # Cart summary component
│   └── checkout_form.py       # Checkout form component
├── services/                  # Business logic services
│   ├── __init__.py
│   └── firebase_service.py    # Firebase service
├── utils/                     # Utility functions
│   ├── __init__.py
│   ├── validators.py          # Input validation utilities
│   └── formatters.py          # Data formatting utilities
└── config/                    # Configuration
    ├── __init__.py
    └── settings.py            # Application settings
```

## Firebase Firestore Structure

### Collections

- **users**: User accounts
  - `uid`: User ID
  - `email`: Email address
  - `display_name`: Display name
  - `cart`: Array of cart items
  - `orders`: Array of order IDs
  - `addresses`: Array of addresses
  - `created_at`: Timestamp

- **products**: Product catalog
  - `name`: Product name
  - `description`: Product description
  - `price`: Product price
  - `category`: Product category
  - `images`: Array of image URLs
  - `stock`: Available stock
  - `active`: Boolean (active/inactive)
  - `rating`: Average rating
  - `reviews_count`: Number of reviews
  - `created_at`: Timestamp
  - `updated_at`: Timestamp

- **orders**: Customer orders
  - `user_id`: User ID
  - `items`: Array of order items
  - `totals`: Order totals (subtotal, tax, shipping, total)
  - `shipping_info`: Shipping address
  - `payment_info`: Payment information
  - `status`: Order status (pending, processing, shipped, delivered, cancelled)
  - `created_at`: Timestamp
  - `updated_at`: Timestamp

## Security Rules

Make sure to configure Firebase Security Rules for production:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    match /products/{productId} {
      allow read: if true;
      allow write: if request.auth != null; // Restrict to admins in production
    }
    match /orders/{orderId} {
      allow read, write: if request.auth != null && 
        (resource == null || resource.data.user_id == request.auth.uid);
    }
  }
}
```

## Usage

1. Sign up or sign in to create an account
2. Browse products on the home page or products page
3. Use the search bar to find specific products
4. Filter products by category
5. Click on a product to view details
6. Add products to your cart
7. Review your cart and proceed to checkout
8. Complete the checkout process with shipping and payment information
9. View your orders in the account section

## Deployment

This application is designed to run 100% in the cloud on Streamlit Cloud. No local execution is required.

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Configure secrets
4. Deploy!

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
