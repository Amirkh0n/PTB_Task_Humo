import config as conf 
import services as ser 
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def admin_msg(update, context, message):
    if context.user_data.get('add')=='categories':
        conf.categories.insert(title=message)
        text=f"{message} nomli kategoriya Muvaffaqiyatli yaratildi!"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton(text='Admin panel', callback_data='back_to_main')]])
        context.user_data['add']=None
    elif context.user_data.get('add', '').startswith('products'):
        pass
    elif context.user_data.get('add')==conf.add_product['title']:
        context.user_data['product_add']['title']=message
        context.user_data['add']=conf.add_product['description']
        text=conf.add_product['description']
        buttons = None 
    elif context.user_data.get('add')==conf.add_product['description']:
        context.user_data['product_add']['description']=message
        context.user_data['add']=conf.add_product['price']
        text=conf.add_product['price']
        buttons = None 
    elif context.user_data.get('add')==conf.add_product['price']:
        context.user_data['product_add']['price']=message
        context.user_data['add']=conf.add_product['count']
        text=conf.add_product['count']
        buttons = None 
    elif context.user_data.get('add')==conf.add_product['count']:
        context.user_data['product_add']['count']=message
        context.user_data['add']=None 
        ser.save_product(context.user_data['product_add'])
        text='Mahsulot Muvaffaqiyatli saqlandi!'
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton(text='Admin panel', callback_data='back_to_main')]])
    else:
        return
    update.message.reply_text(text = text, reply_markup=buttons, parse_mode='HTML')
