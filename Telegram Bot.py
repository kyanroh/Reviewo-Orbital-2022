# import everything
import requests
import logging
from Credentials import BOT_TOKEN, DOCUMENT_PATH 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from MachineLearningModel import MLModel


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Command Handlers
# Sends welcome message
def start(update, context):
    response = ("Welcome to ReviewO! Thanks for using our service!\n\n" + 
                "Please send the input files for Customer Sentiment Analysis in a CSV file\n\n\n" + 
                "/about\n" + 
                "/help")
    update.message.reply_text(response)


# Explains what ReviewO does
def about(update, context):
    response = ("Spending too much time on shopping? Or spending too much time on looking at the reviews to improve your products? " + 
                "At ReviewO, we hope buyers and sellers can automate the process of discovering emotions in reviews " + 
                "so that they can save their time to make faster informed decisions.")
    update.message.reply_text(response)


# Explains instructions for user
def help(update, context):
    response = ("This bot utilises Customer Sentiment Analysis to automate the process of discovering emotions in reviews. " +  
                "You will receive the top 5 words within reviews classified under both good and bad. " +
                "Additionally, the bot can help to filter fake or bot-written reviews and return the file in a .xlsx format. " +  
                "This will provide a quick and accurate overview of the general customer’s sentiments towards a particular product. \n\n" + 
                "You may send the input files for Customer Sentiment Analysis in a .csv or .xlsx file if you have not done so!")
    update.message.reply_text(response)


# Use Machine Learning Model to filter
def filter(update, context):
    mlModel = MLModel(DOCUMENT_PATH)
    response = mlModel.filter()
    update.message.reply_text(response)


# Use Machine Learning Model to conduct CSA
def conductCSA(update, context):
    mlModel = MLModel(DOCUMENT_PATH)
    response = mlModel.conductCSA()
    update.message.reply_text(response)


# Use Machine Learning Model to compile top five words used with the number of times each word is used in reviews 
# for both positive and negative reviews
def compileTopFiveWords(update, context):
    mlModel = MLModel(DOCUMENT_PATH)
    response = mlModel.compileTopFiveWords()
    update.message.reply_text(response)


# Downloads document
def downloadDocument(document):
    file_path = document["file_path"]
    response = requests.get(url=file_path)
    if response.status_code != 200:
        raise FileNotFoundError()
    with open("Reviews.xlsx", 'wb') as document:
        document.write(response.content)


# Check if document is in .CSV/.XLSX
def isCsvOrXlsx(document): 
    return document["file_path"].lower().endswith(('csv', 'xlsx'))


# Handles all document inputs
def documentHandler(update, context):
    document = context.bot.get_file(update.message.document)
    if isCsvOrXlsx(document):
        try:
            downloadDocument(document)
            response = "File Received! Please wait..."
            update.message.reply_text(response)
            
            response = ("Thank you for waiting patiently!\n" + 
                        "What do you wish to do with the reviews? \n\n" + 
                        "/filter\n" +
                        "/conductCSA\n" +
                        "/compileTopFiveWords")
            update.message.reply_text(response)
        except FileNotFoundError:
            response = "File not received. Please try again!"
            update.message.reply_text(response)
    else:
        response = "File not received. Please ensure that the file is in .csv or .xlsx!"
        update.message.reply_text(response)


# Log Errors caused by updates
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# Main
def main():
    updater = Updater(BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add Command Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("about", about))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("filter", filter))
    dp.add_handler(CommandHandler("conductCSA", conductCSA))
    dp.add_handler(CommandHandler("compileTopFiveWords", compileTopFiveWords))

    # Add Messahe Handlers
    dp.add_handler(MessageHandler(Filters.document, documentHandler)) # Listens to documents

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()