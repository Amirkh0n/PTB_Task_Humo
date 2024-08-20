import config as conf 
from telegram import KeyboardButton, ReplyKeyboardMarkup 

def main_menu(update, context, chat_id):
    context.user_data['step'] = conf.STEPS['main_menu']
    user = conf.users.get(id=chat_id, id_column='user_id')
    length = len(conf.orderproduct.get(id=user[3], id_column='order_id', all=True))
        
    context.bot.send_message(
        chat_id = chat_id, 
        text = "Siz asosiy menudasiz!",
        reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text='Shopping'), KeyboardButton(text='Savat(0)')]])
    )
