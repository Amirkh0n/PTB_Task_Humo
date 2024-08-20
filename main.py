from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import commands as comm
import messages as msg
import inlines as inl
import config


def main():
    updater=Updater(token=config.TOKEN)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler('start', comm.start_command))
    dp.add_handler(CommandHandler('admin', comm.admin))
    
    dp.add_handler(MessageHandler(Filters.text, msg.messages))
    dp.add_handler(MessageHandler(Filters.contact, msg.contact))
    dp.add_handler(MessageHandler(Filters.location, msg.location))
    
    dp.add_handler(CallbackQueryHandler(inl.inlines))

    updater.start_polling()
    print("""\t★★★Running bot!!!★★★
》》》to stop -> CTRL + C《《《
""")
    updater.idle()
    print('\t•••STOPPED!!!•••')

if __name__=='__main__':
    main()
 