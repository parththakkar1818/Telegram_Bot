from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

token = "7190983775:AAHTFGuibts5CNlUUL4jA4IHHbzXi7CX8jY"
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}'

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()

# import telegram.ext
# from telegram.ext import Updater, CommandHandler
# from queue import Queue
#
#
# update_queue = Queue() # Create queue instance
# token = "7190983775:AAHTFGuibts5CNlUUL4jA4IHHbzXi7CX8jY"
# updater = telegram.ext.Updater("7190983775:AAHTFGuibts5CNlUUL4jA4IHHbzXi7CX8jY", update_queue=update_queue)
# dispatcher1 = updater.dispatcher
#
# def  start(bot, update):
#     # bot.send_message(update.message.chat_id,"Hello")
#     bot.message.reply_text('Hi! I am parth')
#
# def help(bot, update):
#     update.message.reply_text(
#         """
#         /start -> welcome
#         /help -> what help can i do
#         /content -. to see content
#         """
#     )
#
# def content(bot, update):
#     update.message.reply_text("i am parth from content")
#
# dispatcher.add_handler(telegram.ext.CommandHandler("start", start))
# dispatcher.add_handler(telegram.ext.CommandHandler("help", help))
# dispatcher.add_handler(telegram.ext.CommandHandler("content", content))
#
# updater.start_polling()
# updater.idle()