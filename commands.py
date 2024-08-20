import config as conf 
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup 

# part code
def start_command(update, context):
    user_id = update.message.from_user.id 
    step=context.user_data.get('step', 0)
    
    
    if user_id not in conf.users.get_all_user_id() or step == conf.STEPS['get_phone']:
        conf.users.insert(user_id = user_id, name = update.message.from_user.first_name)
        basket_id = conf.orders.insert(user_id = user_id, status='bascet')
        conf.users.update(id = user_id,  id_column='user_id', bascet=basket_id)
        context.user_data['step'] =conf.STEPS['get_phone']
        update.message.reply_text(
            text = "Assalomu aleykum! Online shop botga xush kelibsiz! \n\nBotdan to'liq foydalanish uchun quyidagi tugma orqali telefon nomerizni yuboring!", 
            reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text="Kontaktni ulashish 📞", request_contact = True)]], resize_keyboard=True)
        )
        return
    user = conf.users.get(id=user_id, id_column='user_id')
    length = len(conf.orderproduct.get(id=user[3], id_column='order_id', all=True))
    
    update.message.reply_text(
        text="Marhamat, o'zingizga kerakli bo'linmi tanlang",
        reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text='Shopping'), KeyboardButton(text=f'Savat({length})')]], resize_keyboard=True)
    )


def admin(update, context):
    user_id = update.message.from_user.id 
    if user_id in conf.get_admins():
        update.message.reply_text(
            text = "Kerakli bo'limni tanlang:",
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(text='Kategoriyalar', callback_data='get_categories'), 
                 # InlineKeyboardButton(text='Mahsulotlar', callback_data='get_products'), 
                 InlineKeyboardButton(text='Buyurtmalar', callback_data='get_orders')
                ],
                [InlineKeyboardButton(text='Foydalanuvchilar', callback_data='get_users')]
            ])
        )
    