# Clothing Rental E-commerce Website

A modern e-commerce website for clothing rental built with Flask and MongoDB Atlas.

## Features

- User authentication (login/register)
- Browse products by category
- Product details and rental functionality
- Responsive design
- MongoDB database integration

## Prerequisites

- Python 3.8 or higher
- MongoDB Atlas account
- pip (Python package manager)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd clothing-rental
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up MongoDB Atlas:
   - Create a MongoDB Atlas account at https://www.mongodb.com/cloud/atlas
   - Create a new cluster
   - Get your connection string
   - Create a `.env` file in the project root and add:
   ```
   MONGODB_URI=your_mongodb_connection_string_here
   ```

5. Run the application:
```bash
python app.py
```

6. Access the website at `http://localhost:5000`

## Project Structure

```
clothing-rental/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── static/            # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── products.html
│   └── product_detail.html
└── README.md
```

## MongoDB Collections

- `users`: Stores user information
- `products`: Stores product information
- `rentals`: Stores rental transactions

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 