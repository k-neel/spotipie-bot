from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, ConversationHandler, Filters, MessageHandler

from sp_bot import dispatcher
from sp_bot import SESSION


PM_MSG = 'Contact me in pm to change your username.'
REG_MSG = 'You need to register first. use /register to get started.'
BOT_URL = 't.me/{}'


# /username command
def getUsername(update: Update, context: CallbackContext) -> None:
    'ask user for usename'
    if update.effective_chat.type != update.effective_chat.PRIVATE:
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Change username", url=BOT_URL.format(context.bot.username))]])
        update.effective_message.reply_text(
            PM_MSG, reply_markup=button)
        return ConversationHandler.END
    update.effective_message.reply_text(
        "Send me a username (max 15 characters)")
    return USERNAME


# username command state
def setUsername(update: Update, context: CallbackContext) -> None:
    'save username in db'
    text = update.effective_message.text.strip()
    if len(text) > 15:
        update.message.reply_text(
            "Invalid username. Try again using /username ")
        return ConversationHandler.END
    elif text.startswith('/'):
        update.message.reply_text(
            "Invalid username. Try again using /username ")
        return ConversationHandler.END
    else:
        try:
            db = SESSION["spotipie"]
            cursor = db["users"]
            tg_id = str(update.message.from_user.id)
            query = {'tg_id': tg_id}
            is_user = cursor.find_one(query)

            if is_user == None:
                update.message.reply_text(REG_MSG)
                SESSION.close()
                return ConversationHandler.END
            else:
                query = {"tg_id": tg_id}
                newvalues = {"$set": {"username": text}}
                cursor.update_one(query, newvalues)
                update.message.reply_text(f"Username updated to {text}")
                SESSION.close()
                return ConversationHandler.END

        except Exception as ex:
            print(ex)
            update.message.reply_text("Database Error")
            return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('Canceled.')
    return ConversationHandler.END


USERNAME = 1
USERNAME_HANDLER = ConversationHandler(
    entry_points=[CommandHandler('name', getUsername)],
    states={USERNAME: [MessageHandler(
            Filters.text & ~Filters.command, setUsername)]},
    fallbacks=[CommandHandler('cancel', cancel)])

dispatcher.add_handler(USERNAME_HANDLER)
