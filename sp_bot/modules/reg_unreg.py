from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackContext, CommandHandler, ConversationHandler

from sp_bot import dispatcher
from sp_bot.modules.db import DATABASE
from sp_bot.modules.misc.request_spotify import SPOTIFY

PM_MSG = 'Contact me in pm to /register or /unregister your account.'
REG_MSG = 'Open the link below, to connect your Spotify account.'
BOT_URL = 't.me/{}'


def register(update: Update, context: CallbackContext) -> None:
    'add new user'
    if update.effective_chat.type == update.effective_chat.PRIVATE:
        tg_id = str(update.effective_user.id)
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Open this link to register", url=SPOTIFY.getAuthUrl())]])
        update.effective_message.reply_text(
            REG_MSG, reply_markup=button)
        return ConversationHandler.END
    else:
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Register here", url=BOT_URL.format(context.bot.username))]])
        update.effective_message.reply_text(
            PM_MSG, reply_markup=button)
        return ConversationHandler.END


def unRegister(update: Update, context: CallbackContext) -> None:
    'add new user'
    if update.effective_chat.type == update.effective_chat.PRIVATE:
        tg_id = str(update.effective_user.id)
        try:
            is_user = DATABASE.fetchData(tg_id)
            if is_user == None:
                update.message.reply_text(
                    "You haven't registered your account yet.")
                return ConversationHandler.END
            else:
                DATABASE.deleteData(tg_id)
                update.message.reply_text("Account successfully removed.")
                return ConversationHandler.END

        except Exception as ex:
            print(ex)
            update.effective_message.reply_text("Database Error.")
            return ConversationHandler.END
    else:
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Contact me in pm", url=BOT_URL.format(context.bot.username))]])
        update.effective_message.reply_text(
            PM_MSG, reply_markup=button)
        return ConversationHandler.END


REGISTER_HANDLER = CommandHandler("register", register)
UNREGISTER_HANDLER = CommandHandler("unregister", unRegister)

dispatcher.add_handler(REGISTER_HANDLER)
dispatcher.add_handler(UNREGISTER_HANDLER)
