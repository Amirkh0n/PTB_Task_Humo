import config as conf
import functions as func 
import services as ser
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# part code
def messages(update, context):
    user_id =update.message.from_user.id
    chat_id = update.effective_chat.id 
    step = context.user_data.get('step', 0)
    message = update.message.text 
    
    if message == 'Shopping':
        func.shop_msg(update, context)
        return 
    elif message.startswith('Savat'):
        user = conf.users.get(id=user_id, id_column='user_id')
        orderproducts = conf.orderproduct.get(id=user[3], id_column='order_id', all=True)
        text = "<b>Savatcha:</b>\n\n" if orderproducts else 'Savatcha bo\'sh'
        if orderproducts:
            total_price = 0
            for i, order_pr in enumerate(orderproducts, start=1):
                total_price += int(order_pr[2])
                product=conf.products.get(id=order_pr[3])
                text+=f"{i}. {product[1]}\n"
                text+=f"   {order_pr[1]} ta \n"
                text+=f"   Narxi: {order_pr[2]:,}\n\n"
            text += f"Jami Summa:  {total_price:,}"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton(text='Sotib olish', callback_data=f"buy_{user[3]}_{total_price}")]]) if orderproducts else None
        update.message.reply_text(text = text, reply_markup=buttons, parse_mode='HTML')
        
        return 
    
    #if step == conf.STEPS['main_menu']:
        #pas
    
    if user_id in conf.get_admins():
        func.admin_msg(update, context, message)

def contact(update, context):
    contact = update.message.contact.phone_number 
    if context.user_data.get('contact'):
        user = conf.users.get(id=update.effective_user.id, id_column='user_id')
        conf.orders.update(id=user[3], phone_number=contact)
        context.bot.send_message(
            chat_id = update.effective_chat.id, 
            text = "Iltimos, mahsulotni yetkazib berishimiz uchun quyidagi tugma orqali joylashuvingizni yuboring:", 
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text='Manzilni yuborish📍', request_location=True)]], resize_keyboard=True)
        )
        del context.user_data['contact']
        context.user_data['location']=True 
        return 
    user_id =update.message.from_user.id 
    contact = update.message.contact.phone_number 
    conf.users.update(id=user_id,  id_column='user_id', phone_number=contact)
    ser.main_menu(update, context, user_id)


def location(update, context):
    if context.user_data.get('location'):
        location = update.message.location
        user = conf.users.get(id=update.effective_user.id, id_column='user_id')
        conf.orders.update(id=user[3], longitude=location.longitude, latitude=location.latitude, status='buy')
        del context.user_data['location']
        orderproducts = conf.orderproduct.get(id=user[3], id_column='order_id', all=True)
        text = "<b>Yangi buyurtma:</b>\n\n"
        text += f"Mijoz: {user[1]}\nBog'lanish uchun +{user[2]}\n"
        if orderproducts:
            total_price = 0
            for i, order_pr in enumerate(orderproducts, start=1):
                total_price += int(order_pr[2])
                product=conf.products.get(id=order_pr[3])
                text+=f"{i}. {product[1]}\n"
                text+=f"   {order_pr[1]} ta \n"
                text+=f"   Narxi: {order_pr[2]:,}\n\n"
            text += f"Jami Summa:  {total_price:,}"
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton(text="Bog'lanish 📞", url=f"https://t.me/+{user[2]}")]]) 
        
        [[context.bot.send_message(
            chat_id = admin,
            text=text, 
            reply_markup = buttons,
            parse_mode = 'HTML'
         ), context.bot.send_location(
             chat_id = admin,
             longitude = location.longitude, 
             latitude = location.latitude, 
         )] for admin in conf.get_admins()]
        id = conf.orders.insert(user_id=user[0], status='bascet')
        conf.users.update(id=user[0], id_column='user_id', bascet = id)
        update.message.reply_text(text='Muvaffaqiyatli bajarildi! Tez orada adminlarimiz siz bilan bog\'lanishadi va buyurtmangiz yetkazib beriladi!', reply_markup=ReplyKeyboardMarkup([[KeyboardButton(text='Shopping'),  KeyboardButton(text='Savat(0)')]], resize_keyboard=True))
        
        