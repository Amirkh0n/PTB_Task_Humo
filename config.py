# config
import json
from database import BaseCRUD 

TOKEN = "5901209945:AAGQqHQmo5xOk-zlWYZJrNQOH48N8FmGoKU"

DB_NAME = 'database/database.db'
users = BaseCRUD(DB_NAME, 'users')
categories = BaseCRUD(DB_NAME, 'categories')
products = BaseCRUD(DB_NAME, 'products')
orders = BaseCRUD(DB_NAME, 'orders')
orderproduct = BaseCRUD(DB_NAME, 'orderproduct')

STEPS = {
    'null': 0,
    'get_phone': 1,
    
    'main_menu':10,
}

add_product = {
    'category': 'Mahsulot qaysi kategoriyaga mansub:\nKarakli kategoriyani tanlang',
    'title': 'Mahsulot nomini kiriting:',
    'description': 'Mahsulotga tavsiv yozing',
    'image': 'Mahsulot rasmini yuboring:',
    'price': 'Mahsulot narxini yozing',
    'count': 'Ushbu mahsulotdan nachta bor:'
}

def get_admins():
    with open('database/admins.json', 'r') as file:
        return json.load(file)

def save_admins(list_id):
        with open('database/admins.json', 'w') as file:
            json.dump(list_id, file) 
        