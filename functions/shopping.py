import config as conf 
import services as ser 
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def shop_msg(update, context):
    text = "<b>Marhamat kerkali kategoriyani tanlang:</b>\n\n"
    buttons = []
    for i, category in enumerate(conf.categories.get_all(),  start=1):
        text += f"{i}. {category[1]}\n"
        buttons.append(InlineKeyboardButton(text=str(i), callback_data = f'shop_category_{category[0]}'))
    update.message.reply_text(
        text=text, 
        reply_markup=InlineKeyboardMarkup(ser.list_page(buttons, 5)),
        parse_mode='HTML'
    )