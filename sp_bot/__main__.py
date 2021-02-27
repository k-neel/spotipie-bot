import importlib

from telegram import Message, Chat, Update, Bot, User
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, Filters, MessageHandler, CallbackQueryHandler, CallbackContext
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop, Dispatcher
from telegram.utils.helpers import escape_markdown

from sp_bot import dispatcher, updater, LOGGER, TOKEN, CLIENT_ID, CLIENT_SECRET, OWNER
from sp_bot.modules import ALL_MODULES


START_TEXT = '''
Hi {},

Follow these steps to start using the bot -
1. Use /register to connect your spotify account with this bot.
2. Open the provided link, after you see a successful message come back here &
3. then use /name to set your username.

thats it! you can then share your song status using /now
or using the inline query @spotipiebot

use /help to get the list of commands.
'''

HELP_TEXT = '''
Heres the list of commands -

/now - share currently playing song on spotify.
/name - change your username.
/unregister - to unlink your spotify account from the bot.
/register - to connect your spotify account with the bot.
@spotipiebot - share song using inline query
'''

IMPORTED = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("sp_bot.modules." + module_name)

    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception(
            "Can't have two modules with the same name! Please change one")


# /start command
def start(update: Update, context: CallbackContext):
    if update.effective_chat.type == update.effective_chat.PRIVATE:
        first_name = update.effective_user.first_name
        text = update.effective_message.text
        if len(text) <= 7:
            update.effective_message.reply_text(
                START_TEXT.format(first_name), parse_mode=ParseMode.MARKDOWN)
        elif text.endswith('register'):
            update.message.reply_text(
                "To register your account use /register command.")
        elif text.endswith('username'):
            update.message.reply_text(
                "To change your username use /name command.")
        elif text.endswith('token'):
            update.message.reply_text(
                "use /unregister to unlink your account & register again using /register command.")
        elif text.endswith('notsure'):
            update.message.reply_text("I'm not sure what you're listening to.")
        elif text.endswith('ads'):
            update.message.reply_text(
                "You're listening to ads!")
        elif text.endswith('notlistening'):
            update.message.reply_text(
                "You're not listening to anything on Spotify at the moment.")
        else:
            update.effective_message.reply_text(
                START_TEXT.format(first_name), parse_mode=ParseMode.MARKDOWN)

        update.effective_message.delete()
        return
    else:
        update.effective_message.reply_text("Hmm?")


# /help command
def get_help(update: Update, context: CallbackContext):
    # ONLY send help in PM
    if update.effective_chat.type != update.effective_chat.PRIVATE:
        update.effective_message.reply_text("Contact me in PM to get the list of possible commands.",
                                            reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton(text="Help",
                                                                       url="t.me/{}?start=help".format(
                                                                           context.bot.username))]]))
        return

    else:
        update.effective_message.reply_text(
            HELP_TEXT, parse_mode=ParseMode.MARKDOWN)


# main
def main():
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", get_help)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()
