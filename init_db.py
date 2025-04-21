from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# MongoDB connection with error handling
try:
    # Create a new client and connect to the server
    client = MongoClient(
        "mongodb+srv://akrutidabas10:PqVtgLfMgcXB0ZNU@cluster0.avw8ttg.mongodb.net/?retryWrites=true&w=majority",
        connectTimeoutMS=30000,
        socketTimeoutMS=45000
    )
    
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
    
    db = client['clothing_rental']
    products = db.products
    users = db.users
    rentals = db.rentals
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise

# Clear existing collections
products.delete_many({})
users.delete_many({})
rentals.delete_many({})

# Sample products with more details
sample_products = [
    {
        'name': 'Elegant Evening Gown',
        'description': 'Beautiful black evening gown perfect for formal events. Made with premium silk fabric and intricate beadwork.',
        'price': 50,
        'category': 'formal',
        'stock': 5,
        'size': ['S', 'M', 'L'],
        'color': 'Black',
        'material': 'Silk',
        'brand': 'Luxury Couture',
        'image_url': 'https://www.frontierraas.com/pub/media/catalog/product/cache/74910300c4c00f257771c5afa25168a6/f/r/fr_gown_18_.jpg',
        'created_at': datetime.now()
    },
    {
        'name': 'Casual Summer Dress',
        'description': 'Light and comfortable summer dress perfect for beach outings and casual gatherings.',
        'price': 25,
        'category': 'casual',
        'stock': 8,
        'size': ['XS', 'S', 'M', 'L'],
        'color': 'Blue',
        'material': 'Cotton',
        'brand': 'Summer Breeze',
        'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1zTtMpzbljjLF2iQLOcvMWzpYnqR-K6hfUw&s',
        'created_at': datetime.now()
    },
    {
        'name': 'Party Jumpsuit',
        'description': 'Trendy jumpsuit for parties and events. Features a flattering cut and comfortable fit.',
        'price': 35,
        'category': 'party',
        'stock': 6,
        'size': ['S', 'M', 'L'],
        'color': 'Red',
        'material': 'Polyester',
        'brand': 'Party Wear',
        'image_url': 'https://assets.myntassets.com/w_412,q_60,dpr_2,fl_progressive/assets/images/25229024/2023/10/5/cebc02d2-d3c2-473d-9e56-cb90fb9ed6121696491498260GlobusBlackBasicJumpsuit1.jpg',
        'created_at': datetime.now()
    },
    {
        'name': 'Business Suit',
        'description': 'Professional business suit for formal occasions. Includes jacket and pants.',
        'price': 45,
        'category': 'formal',
        'stock': 4,
        'size': ['M', 'L', 'XL'],
        'color': 'Navy Blue',
        'material': 'Wool',
        'brand': 'Executive Style',
        'image_url': 'https://www.frontierraas.com/pub/media/catalog/product/cache/74910300c4c00f257771c5afa25168a6/f/r/fr_gown_18_.jpg',
        'created_at': datetime.now()
    },
    {
        'name': 'Casual Jeans',
        'description': 'Comfortable and stylish jeans perfect for everyday wear.',
        'price': 20,
        'category': 'casual',
        'stock': 10,
        'size': ['28', '30', '32', '34'],
        'color': 'Blue',
        'material': 'Denim',
        'brand': 'Denim Co.',
        'image_url': 'https://www.frontierraas.com/pub/media/catalog/product/cache/74910300c4c00f257771c5afa25168a6/f/r/fr_gown_18_.jpg',
        'created_at': datetime.now()
    },
    {
        'name': 'Cocktail Dress',
        'description': 'Elegant cocktail dress for special occasions. Features a flattering silhouette.',
        'price': 40,
        'category': 'party',
        'stock': 7,
        'size': ['XS', 'S', 'M'],
        'color': 'Emerald Green',
        'material': 'Satin',
        'brand': 'Evening Elegance',
        'image_url': 'https://5.imimg.com/data5/UD/IR/MY-3624146/women-business-suit.jpg',
        'created_at': datetime.now()
    },
    {
        'name': 'Formal Blazer',
        'description': 'Classic formal blazer perfect for business meetings and formal events.',
        'price': 55,
        'category': 'formal',
        'stock': 3,
        'size': ['M', 'L', 'XL'],
        'color': 'Charcoal',
        'material': 'Wool Blend',
        'brand': 'Professional Wear',
        'image_url': 'https://5.imimg.com/data5/UD/IR/MY-3624146/women-business-suit.jpg',
        'created_at': datetime.now()
    },
    {
        'name': 'Summer T-Shirt',
        'description': 'Comfortable cotton t-shirt perfect for summer days.',
        'price': 15,
        'category': 'casual',
        'stock': 12,
        'size': ['S', 'M', 'L', 'XL'],
        'color': 'White',
        'material': 'Cotton',
        'brand': 'Summer Basics',
        'image_url': 'https://www.frontierraas.com/pub/media/catalog/product/cache/74910300c4c00f257771c5afa25168a6/f/r/fr_gown_18_.jpg',
        'created_at': datetime.now()
    }
]

# Sample admin user
admin_user = {
    'name': 'Admin User',
    'email': 'admin@rental.com',
    'password': 'admin123',  # Note: In production, this should be hashed
    'role': 'admin',
    'created_at': datetime.now()
}

try:
    # Insert sample products
    products.insert_many(sample_products)
    print("Sample products added successfully!")
    
    # Insert admin user
    users.insert_one(admin_user)
    print("Admin user added successfully!")
    
    print("\nDatabase initialized with:")
    print(f"- {len(sample_products)} products")
    print(f"- 1 admin user")
    print(f"- Empty rentals collection")
    
except Exception as e:
    print(f"Error adding data to database: {e}") 