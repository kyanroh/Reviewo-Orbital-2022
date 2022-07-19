# Import everything
import requests
import logging
from Credentials import BOT_TOKEN
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from DistilBERT_Model import Distilbert
import os
import pandas as pd

# Downloads xlsx document
def download_xlsx(document):
    file_path = document["file_path"]
    response = requests.get(url=file_path)
    if response.status_code != 200:
        raise FileNotFoundError()
    with open("Reviews.xlsx", 'wb') as document:
        document.write(response.content)


# Downloads csv document
def download_csv(document):
    file_path = document["file_path"]
    response = requests.get(url=file_path)
    if response.status_code != 200:
        raise FileNotFoundError()
    with open("Reviews.csv", 'wb') as document:
        document.write(response.content)


# Check if document is in .CSV/.XLSX
def is_csv(document): 
    return document["file_path"].lower().endswith(('csv'))


# Check if document is in .CSV/.XLSX
def is_xlsx(document): 
    return document["file_path"].lower().endswith(('xlsx'))


class ReviewoBot:
    def __init__(self):
        self.model = None
        self.document_path = ""
    
    # Command Handlers
    # Sends welcome message
    def start(self, update, context):
        response = ("Welcome to ReviewO! Thanks for using our service!\n\n" + 
                    "Please send the input files for Customer Sentiment Analysis in a CSV or XLSX file\n\n" + 
                    "/about\n" + 
                    "/help")
        update.message.reply_text(response)


    # Explains what ReviewO does
    def about(self, update, context):
        response = ("Spending too much time on shopping? Or spending too much time on looking at the reviews to improve your products? " + 
                    "At ReviewO, we hope buyers and sellers can automate the process of discovering emotions in reviews " + 
                    "so that they can save their time to make faster informed decisions.")
        update.message.reply_text(response)


    # Explains instructions for user
    def help(self, update, context):
        response = ("This bot utilises Customer Sentiment Analysis to automate the process of discovering emotions in reviews. " +  
                    "You will receive the top 5 words within reviews classified under both good and bad. " +
                    "Additionally, the bot can help to filter fake or bot-written reviews and return the file in a .xlsx format. " +  
                    "This will provide a quick and accurate overview of the general customer’s sentiments towards a particular product. \n\n" + 
                    "You may send the input files for Customer Sentiment Analysis in a .csv or .xlsx file if you have not done so!")
        update.message.reply_text(response)

    # Use Machine Learning Model to filter
    def filter(self, update, context):
        self.wait(update)
        chat_id = update.message.chat_id
        response_df, new_model = self.model.filter()
        self.model = new_model
        response_df.to_excel("filtered_reviews.xlsx", index=False)
        with open("filtered_reviews.xlsx", "rb") as reponse_file:
            context.bot.send_document(chat_id, reponse_file)
        self.thank_user(update)

    # Use Machine Learning Model to conduct CSA
    def retrieve_predictions(self, update, context):
        self.wait(update)
        chat_id = update.message.chat_id
        response_df, new_model = self.model.conduct_CSA()
        self.model = new_model
        response_df.to_excel("predicted_reviews.xlsx", index=False)
        with open("predicted_reviews.xlsx", "rb") as reponse_file:
            context.bot.send_document(chat_id, reponse_file)
        self.thank_user(update)

    # Sort predicted reviews into good and bad
    def sort_predicted(self, update, context):
        predicted_reviews = self.model.get_predicted_reviews()
        if not self.model.has_predicted():
            predicted_reviews, new_model = self.model.conduct_CSA()
            self.model = new_model
        self.wait(update)
        chat_id = update.message.chat_id
        good_reviews, bad_reviews = self.model.sort_predicted_reviews(predicted_reviews)
        good_reviews.to_excel("good_reviews.xlsx", index=False)
        bad_reviews.to_excel("bad_reviews.xlsx", index=False)
        with open("good_reviews.xlsx", "rb") as reponse_file:
            context.bot.send_document(chat_id, reponse_file)
        with open("bad_reviews.xlsx", "rb") as reponse_file:
            context.bot.send_document(chat_id, reponse_file)
        self.thank_user(update)

    # Use Machine Learning Model to compile top five words used with the number of times each word is used in reviews 
    # for both positive and negative reviews
    def compile_top_five_words(self, update, context):
        self.wait(update)
        response = ""
        response_dict, new_model = self.model.compile_top_five_words()
        self.model = new_model
        response = ""
        for sentiment, words in response_dict.items():
            response += (sentiment + ":\n\n") 
            for word in words:
                response += (word + "\n")
            response += "\n\n"

        update.message.reply_text(response)
        self.thank_user(update)

    # Updates message after successful download of file 
    def choose_catgeory(self, update):
        response = ("Please choose your product category: \n\n" + 
                    "/general")
        update.message.reply_text(response)

    # Initiates model for general product category 
    def general(self, update, context):
        self.wait(update)
        self.model = Distilbert(self.document_path)
        self.choose_function(update)

    # Allows user to choose function
    def choose_function(self, update):
        response = ("What do you wish to do with the reviews? \n\n" + 
                    "/filter_fake_reviews\n" +
                    "/retrieve_predictions\n" +
                    "/sort_predicted_reviews\n" +
                    "/compile_top_five_words")
        update.message.reply_text(response)
    
    # Waiting message
    def wait(self, update):
        response = "Please wait..."
        update.message.reply_text(response)

    # Thank user
    def thank_user(self, update):
        response = ("Thank you for using ReviewO bot.\n\n" + 
                    "Use a new set of reviews:\n" + 
                    "/use_new_reviews\n\n" + 
                    "Use current set of reviews:\n"
                    "/filter_fake_reviews\n" +
                    "/retrieve_predictions\n" +
                    "/sort_predicted_reviews\n" +
                    "/compile_top_five_words")
        update.message.reply_text(response)

    # Prompt user to send new set of reviews 
    def use_new_reviews(self, update, context):
        response = "Please send the new set of reviews"
        update.message.reply_text(response)

    # Check if downloaded document is in correct format
    def is_correct_format(self, document):
        if is_csv(document):
            df = pd.read_csv(self.document_path)
            return "Reviews" in df.columns.to_list()
        else:
            df = pd.read_excel(self.document_path)
            return "Reviews" in df.columns.to_list()
            
    # Handles all document inputs
    def handle_document(self, update, context):
        document = context.bot.get_file(update.message.document)
        self.wait(update)
        if is_csv(document):
            try:
                download_csv(document)
                self.document_path = os.path.dirname(__file__) + '/' + "Reviews.csv"
                if self.is_correct_format(document):
                    response = "File received! Thank you for waiting patiently!"
                    update.message.reply_text(response)
                    self.choose_catgeory(update)
                else:
                    response = "File is not in correct format! Please make sure that the file has a column name 'Reviews' !"
                    update.message.reply_text(response)
                
            except FileNotFoundError:
                response = "File not received. Please try again!"
                update.message.reply_text(response)
        elif is_xlsx(document):
            try:
                download_xlsx(document)
                self.document_path = os.path.dirname(__file__) + '/' + "Reviews.xlsx"
                if self.is_correct_format(document):
                    response = "File received! Thank you for waiting patiently!"
                    update.message.reply_text(response)
                    self.choose_catgeory(update)
                else:
                    response = "File is not in correct format! Please make sure that the file has a column name 'Reviews' !"
                    update.message.reply_text(response)
                
            except FileNotFoundError:
                response = "File not received. Please try again!"
                update.message.reply_text(response)
        else:
            response = "File not received. Please ensure that the file is in .csv or .xlsx!"
            update.message.reply_text(response)


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

    #Create ReviewoBot object
    reviewo_bot = ReviewoBot()

    # Add Command Handlers
    dp.add_handler(CommandHandler("start", reviewo_bot.start))
    dp.add_handler(CommandHandler("about", reviewo_bot.about))
    dp.add_handler(CommandHandler("help", reviewo_bot.help))
    dp.add_handler(CommandHandler("filter_fake_reviews", reviewo_bot.filter))
    dp.add_handler(CommandHandler("use_new_reviews", reviewo_bot.use_new_reviews))
    dp.add_handler(CommandHandler("retrieve_predictions", reviewo_bot.retrieve_predictions))
    dp.add_handler(CommandHandler("sort_predicted_reviews", reviewo_bot.sort_predicted))
    dp.add_handler(CommandHandler("compile_top_five_words", reviewo_bot.compile_top_five_words))
    dp.add_handler(CommandHandler("general", reviewo_bot.general))


    # Add Messahe Handlers
    dp.add_handler(MessageHandler(Filters.document, reviewo_bot.handle_document)) # Listens to documents

    # Log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()