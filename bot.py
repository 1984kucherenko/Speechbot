from telegram import Update,InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes,MessageHandler, filters, ConversationHandler, CallbackQueryHandler
from voice import text_to_file
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
TIME_STEP,TYPE_STATE = range(2)

main_keyboard = ReplyKeyboardMarkup(
    [["Sign_in", "Help"]],
    resize_keyboard=True,   # робить клавіатуру компактною
    one_time_keyboard=False # клавіатура завжди лишається
)
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text == "Sign_in":
        await start(update,context)
    elif text == "Help":
        await help_command(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Це бот для запису на заняття.\n"
        "Натисни 'Start', щоб почати запис.\n"
        "Або 'Help', щоб отримати підказку.",
        reply_markup=main_keyboard
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send message on `/start`."""
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("18:00", callback_data="18:00"),
            InlineKeyboardButton("21:00", callback_data="21:00"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text(f'Hello {update.effective_user.first_name}, please choose time', reply_markup=reply_markup)
    return TIME_STEP

async def handle_time (update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer() #must for buttons
    # add data to dictionary
    context.user_data['time']  = query.data
 
    # change buttons to choose activity
    keyboard = [
        [
            InlineKeyboardButton("Boxing", callback_data="Boxing"),
            InlineKeyboardButton("Swimming", callback_data="Swimming"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await query.edit_message_text(f'Excelent {update.effective_user.first_name}, you choose {query.data}, please choose activity', reply_markup=reply_markup)
    return TYPE_STATE

async def handle_activity(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    query = update.callback_query
    await query.answer() #must for buttons

    context.user_data['training']  = query.data

    # get all data from dic
    user_info = context.user_data
     
    # Send message with text and appended InlineKeyboard
    await query.edit_message_text(f'All done!\nTraining: {user_info['training']}\nTime :{user_info['time']}')
    context.user_data.clear()
    # show main menu
    await query.message.reply_text(
        "Що хочеш зробити далі?",
        reply_markup=main_keyboard
    )
    return ConversationHandler.END

async def help_hendler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(""" Цей бот може перетворити звичайне текстове повідомлення на аудіо повідомлення. Очікую на будь-який текст.""")

async def reply_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text("Озвучимо текст: " + update.message.text)

async def reply_message_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    file_name = text_to_file(update.message.text)
    await update.message.reply_voice(voice= open(file_name,"rb"))

app = ApplicationBuilder().token(TOKEN).build()

# app.add_handler(CommandHandler("hello", hello))
# app.add_handler(CommandHandler("start", start))
conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start), MessageHandler(filters.Regex("^Sign_in$"), start)],
        states={
            TIME_STEP:[CallbackQueryHandler(handle_time)],
            TYPE_STATE:[CallbackQueryHandler(handle_activity)]
        },
        fallbacks=[],
)
app.add_handler(conv_handler)
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
# app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_text))
#app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,reply_message_voice))

app.run_polling()
