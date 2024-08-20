import services as ser
import config as conf 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton 

# part code
def inlines(update, context):
    query = update.callback_query 
    user_id =query.from_user.id 
     
    if query.data.startswith('shop'):
        spl = query.data.split('_')
        if spl[1]=='category':
            text="<b>Mahsulotlar: </b>\n\n"
            buttons = []
            for i, product in enumerate(conf.products.get(id=spl[2], id_column='category_id', all=True),  start=1):
                text += f"{i}. {product[1]}\n"
                buttons.append(InlineKeyboardButton(text=str(i), callback_data = f'shop_product_{product[0]}'))
            query.edit_message_text(
                text=text, 
                reply_markup=InlineKeyboardMarkup(ser.list_page(buttons, 5)+[[InlineKeyboardButton(text='Orqaga', callback_data='back_to_shop_category')]]),
                parse_mode = 'HTML'
            )
        elif spl[1]=='product':
            product = conf.products.get(id=spl[2])
            text=f"<b>{product[1]}</b>\n\n{product[2]}\n\nNarxi: {product[4]:,} so'm"
            
            query.edit_message_text(
                text=text, 
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        text='Savatga qo\'shish', callback_data = f'basket_{product[0]}'
                    ),
                    InlineKeyboardButton(
                        text='Orqaga', 
                        callback_data=f'back_to_shop_products_{spl[2]}'
                    )
                ]]),
                parse_mode = 'HTML'
            )
    elif query.data.startswith('basket'):
        id = query.data.split('_')[1]
        product = conf.products.get(id)
        text=f"<b>{product[1]}</b>\nNarxi: {product[4]:,} so'm\n\nSavatga 1ta saqlanmoqda!"
        buttons = [
            [InlineKeyboardButton(text='➖', callback_data=f'minus_{id}_1'), InlineKeyboardButton(text='Saqlash', callback_data=f'save_{id}_1'), InlineKeyboardButton(text='➕', callback_data=f'plus_{id}_1')],
            [InlineKeyboardButton(text='Orqaga', callback_data='back_to_shop_category')]
        ]
        query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(buttons),  parse_mode='HTML')

    elif query.data.startswith('plus'):
        id = query.data.split('_')[1]
        product = conf.products.get(id)
        count=int(query.data.split('_')[2])+1
        text=f"<b>{product[1]}</b>\nNarxi: {product[4]:,} so'm\n\nSavatga {count}ta saqlanmoqda!"
        buttons = [
            [InlineKeyboardButton(text='➖', callback_data=f'minus_{id}_{count}'), InlineKeyboardButton(text='Saqlash', callback_data=f'save_{id}_{count}'), InlineKeyboardButton(text='➕', callback_data=f'plus_{id}_{count}')],
            [InlineKeyboardButton(text='Orqaga', callback_data='back_to_shop_category')]
        ]
        query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(buttons),  parse_mode='HTML')

    elif query.data.startswith('minus'):
        id = query.data.split('_')[1]
        product = conf.products.get(id)
        count=int(query.data.split('_')[2])-1
        if count < 1:
            query.answer(text="Buyurtma berish uchun kamida 1ta mahsulot bo'lishi kerak!", show_alert =True) 
            return 
        text=f"<b>{product[1]}</b>\nNarxi: {product[4]:,} so'm\n\nSavatga {count}ta saqlanmoqda!"
        buttons = [
            [InlineKeyboardButton(text='➖', callback_data=f'minus_{id}_{count}'), InlineKeyboardButton(text='Saqlash', callback_data=f'save_{id}_{count}'), InlineKeyboardButton(text='➕', callback_data=f'plus_{id}_{count}')],
            [InlineKeyboardButton(text='Orqaga', callback_data='back_to_shop_category')]
        ]
        query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(buttons),  parse_mode='HTML')

    elif query.data.startswith('save'):
        spl=query.data.split('_')
        user = conf.users.get(id=user_id, id_column='user_id')
        bascet = conf.orders.get(id = user[3])
        product = conf.products.get(int(spl[1]))
        id = conf.orderproduct.insert(
            count=spl[2], 
            price = int(spl[2])*int(product[4]), 
            product_id = product[0], 
            order_id=bascet[0]
        )
        length = len(conf.orderproduct.get(id=user[3], id_column='order_id', all=True))
        
        text='Amaliyot muvaffaqiyatli bajarildi!'
        buttons = [[KeyboardButton(text='Shopping'), KeyboardButton(text=f'Savat({length})')]]
        query.edit_message_text(
            text=text,
        )
        context.bot.send_message(
            chat_id = user_id, 
            text = 'Kerakli bo\'limni tanlang: ',
            reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard =True)
        )
        
    elif query.data.startswith('buy'):
        spl = query.data.split('_')
        query.edit_message_text(text = f"Umumiy Summa: {int(spl[2]):,} so'm")
        context.user_data['contact']=True 
        context.bot.send_message(
            chat_id = user_id, 
            text = "Iltimos siz bilan aloqaga chiqishimiz uchun 'Kontaktni ulashish 📞' tugmasini bosing!",
            reply_markup = ReplyKeyboardMarkup([[KeyboardButton(text ='Kontaktni ulashish 📞', request_contact=True)]],  resize_keyboard=True)
        )
    
        ### Admin panel ###
    elif query.data.startswith('get'):
        models = query.data.split('_')
         
        if models[1]=='categories':
             model = conf.categories.get_all()
             text = "<b>Kategoriyalar:</b>\n\n"
        elif models[1]=='products':
             model = conf.products.get_all()
             text = "<b>Mahsulotlar:</b>\n\n"
        else:
             query.answer(text="Noma'lum buyruq!")
             return 
             
        buttons = []
        for i, val in enumerate(model, start=1):
             text += f"{i}. {val[1]}\n"
             buttons.append(InlineKeyboardButton(text =str(i), callback_data=f"{models[1]}_{val[0]}"))
        btn=ser.list_page(buttons, 5)
        btn.append([InlineKeyboardButton(text='Qo\'shish', callback_data=f'add_{models[1]}'), InlineKeyboardButton(text="Orqaga", callback_data='back_to_main')])
        query.edit_message_text(
             text = text, 
             reply_markup = InlineKeyboardMarkup(btn),
             parse_mode = 'HTML'
        )
    
    elif query.data.startswith('add'):
        models = query.data.split('_')
         
        if models[1]=='categories':
             context.user_data['add']=models[1]
             text = "Kategoriya nomini kiriting!"
        elif models[1]=='products':
             context.user_data['add']=conf.add_product['title']
             context.user_data['product_add']={'category_id':models[2]} if len(models)==3 else {}
             text = conf.add_product['title']
        else:
             query.answer(text="Noma'lum buyruq!")
             return
        query.edit_message_text(text=text)
    
    elif query.data.startswith('categories'):
        id = query.data.split('_')[1]
        products = conf.products.get(id=id, id_column='category_id', all=True)
        text="Mahsulotlar:\n\n"
        buttons = []
        for i, val in enumerate(products, start=1):
             text += f"{i}. {val[1]}\n"
             buttons.append(InlineKeyboardButton(text=str(i), callback_data=f"products_{val[0]}"))
        btn=ser.list_page(buttons, 5)
        btn.append([InlineKeyboardButton(text='Qo\'shish', callback_data= f'add_products_{id}'), InlineKeyboardButton(text="Orqaga", callback_data='get_categories')])
        query.edit_message_text(
             text = text, 
             reply_markup = InlineKeyboardMarkup(btn),
             parse_mode = 'HTML'
        )
    elif query.data.startswith('back'):
        back_to = query.data.split('_')
        
        if back_to[2] == 'main':
            query.edit_message_text(
                text = "Kerakli bo'limni tanlang:",
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(text='Kategoriyalar', callback_data='get_categories'), InlineKeyboardButton(text='Mahsulotlar', callback_data='get_products'), InlineKeyboardButton(text='Buyurtmalar', callback_data='get_orders')],
                    [InlineKeyboardButton(text='Foydalanuvchilar', callback_data='get_users')]
                ])
            )
        elif back_to[2]=='shop' and back_to[3]=='category':
            text = "<b>Marhamat kerkali kategoriyani tanlang:</b>\n\n"
            buttons = []
            for i, category in enumerate(conf.categories.get_all(),  start=1):
                text += f"{i}. {category[1]}\n"
                buttons.append(InlineKeyboardButton(text=str(i), callback_data = f'shop_category_{category[0]}'))
            query.edit_message_text(
                text=text, 
                reply_markup=InlineKeyboardMarkup(ser.list_page(buttons, 5)),
                parse_mode='HTML'
            )
        elif back_to[2]=='shop' and back_to[3]=='products': 
            text="<b>Mahsulotlar: </b>\n\n"
            buttons = []
            for i, product in enumerate(conf.products.get(id=back_to[4], id_column='category_id', all=True),  start=1):
                text += f"{i}. {product[1]}\n"
                buttons.append(InlineKeyboardButton(text=str(i), callback_data = f'shop_product_{product[0]}'))
            query.edit_message_text(
                text=text, 
                reply_markup=InlineKeyboardMarkup(ser.list_page(buttons, 5)+[[InlineKeyboardButton(text='Orqaga', callback_data='back_to_shop_category')]]),
                parse_mode = 'HTML'
            )
        
