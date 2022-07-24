# Import everything
import logging
from Credentials import BOT_TOKEN
from UserGuide.UserGuide import UserGuide
from Authentication import Signup, Login, Logout
from ReviewoBot import ReviewoBot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Log Errors caused by updates
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# Main
def main():
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Create ReviewoBot object
    reviewo_bot = ReviewoBot()
    user_guide = UserGuide(reviewo_bot)
   
    login = Login()
    signup = Signup()
    logout = Logout()

    # Add Command Handlers
    dp.add_handler(login.convo_handler)
    dp.add_handler(signup.convo_handler)
    dp.add_handler(CommandHandler("logout", logout.logout))
    # dp.add_handler(delete.convo_handler)
    
    # Each function below will check for auth.login_status:
    dp.add_handler(CommandHandler("start", reviewo_bot.start))
    dp.add_handler(CommandHandler("about", reviewo_bot.about))
    dp.add_handler(CommandHandler("help", reviewo_bot.help))
    dp.add_handler(CommandHandler("filter_fake_reviews", reviewo_bot.filter))
    dp.add_handler(CommandHandler("use_new_reviews", reviewo_bot.use_new_reviews))
    dp.add_handler(CommandHandler("retrieve_predictions", reviewo_bot.retrieve_predictions))
    dp.add_handler(CommandHandler("sort_predicted_reviews", reviewo_bot.sort_predicted))
    dp.add_handler(CommandHandler("compile_top_five_words", reviewo_bot.compile_top_five_words))
    dp.add_handler(CommandHandler("general", reviewo_bot.general))
    dp.add_handler(CommandHandler("start_tutorial", user_guide.start_tutorial))
    dp.add_handler(CommandHandler("end_tutorial", user_guide.end_tutorial))
    dp.add_handler(CommandHandler("next", user_guide.next))



    # # Add Messahe Handlers
    dp.add_handler(MessageHandler(Filters.document, reviewo_bot.handle_document)) # Listens to documents

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()