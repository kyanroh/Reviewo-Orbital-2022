from DistilBERT_Model import Distilbert
import requests
import pandas as pd
from database import storage
from Authentication import current_users


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

# Uploads csv document
def upload_csv(document, username):
    file_path = document["file_path"]
    response = requests.get(url=file_path)
    if response.status_code != 200:
        raise FileNotFoundError()
    try:
        cloud_file_name = f"{username}/Reviews.csv"
        storage.child(cloud_file_name).put(response.content)
    except Exception as e:
        print(e)


# Check if document is in .CSV/.XLSX
def is_csv(document): 
    return document["file_path"].lower().endswith(('csv'))


# Check if document is in .CSV/.XLSX
def is_xlsx(document): 
    return document["file_path"].lower().endswith(('xlsx'))


class ReviewoBot:
    def __init__(self):
        self.models = {}
    
    # Check log in status
    def is_logged_in(self, update):
        chat_id = update.message.chat_id
        return chat_id in current_users.keys()

    # Command Handlers
    # Sends welcome message
    def start(self, update, context):
        response = ("Welcome to ReviewO!\n\n" + 
                    "/login\n" + 
                    "/signup\n" + 
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
                    "You may send the input files for Customer Sentiment Analysis in a .csv or .xlsx file if you have not done so!" + 
                    "\n\n/start_tutorial")
        update.message.reply_text(response)

    # Use Machine Learning Model to filter
    def filter(self, update, context):
        if self.is_logged_in(update):
            self.wait(update)
            chat_id = update.message.chat_id
            response_df, new_model = self.models[chat_id].filter()
            self.models[chat_id] = new_model

            chat_id = update.message.chat_id
            username = current_users[chat_id]["email"]
            response_df.to_excel(f"{username}/filtered_reviews.xlsx", index=False)

            with open(f"{username}/filtered_reviews.xlsx", "rb") as response_file:
                context.bot.send_document(chat_id, response_file)
            self.thank_user(update)
        else:
            response = "You are currently not logged in, please log in! \n\n/login"
            update.message.reply_text(response)

    # Use Machine Learning Model to conduct CSA
    def retrieve_predictions(self, update, context):
        if self.is_logged_in(update):
            self.wait(update)
            chat_id = update.message.chat_id
            response_df, new_model = self.models[chat_id].conduct_CSA()
            self.models[chat_id] = new_model

            chat_id = update.message.chat_id
            username = current_users[chat_id]["email"]
            response_df.to_excel(f"{username}/predicted_reviews.xlsx", index=False)
            
            with open(f"{username}/predicted_reviews.xlsx", "rb") as response_file:
                context.bot.send_document(chat_id, response_file)
            self.thank_user(update)
        else:
            response = "You are currently not logged in, please log in! \n\n/login"
            update.message.reply_text(response)

    # Sort predicted reviews into good and bad
    def sort_predicted(self, update, context):
        if self.is_logged_in(update):
            chat_id = update.message.chat_id
            predicted_reviews = self.models[chat_id].get_predicted_reviews()
            if not self.models[chat_id].has_predicted():
                predicted_reviews, new_model = self.models[chat_id].conduct_CSA()
                self.models[chat_id] = new_model
            self.wait(update)
            good_reviews, bad_reviews = self.models[chat_id].sort_predicted_reviews(predicted_reviews)

            chat_id = update.message.chat_id
            username = current_users[chat_id]["email"]
            good_reviews.to_excel(f"{username}/good_reviews.xlsx", index=False)
            bad_reviews.to_excel(f"{username}/bad_reviews.xlsx", index=False)
            
            with open(f"{username}/good_reviews.xlsx", "rb") as response_file:
                context.bot.send_document(chat_id, response_file)
            with open(f"{username}/bad_reviews.xlsx", "rb") as response_file:
                context.bot.send_document(chat_id, response_file)
            self.thank_user(update)
        else:
            response = "You are currently not logged in, please log in! \n\n/login"
            update.message.reply_text(response)

    # Use Machine Learning Model to compile top five words used with the number of times each word is used in reviews 
    # for both positive and negative reviews
    def compile_top_five_words(self, update, context):
        if self.is_logged_in(update):
            chat_id = update.message.chat_id
            self.wait(update)
            response = ""
            response_dict, new_model = self.models[chat_id].compile_top_five_words()
            self.models[chat_id] = new_model
            response = ""
            for sentiment, words in response_dict.items():
                response += (sentiment + ":\n\n") 
                for word in words:
                    response += (word + "\n")
                response += "\n\n"

            update.message.reply_text(response)
            self.thank_user(update)
        else:
            response = "You are currently not logged in, please log in! \n\n/login"
            update.message.reply_text(response)

    # Updates message after successful download of file 
    def choose_catgeory(self, update):
        response = ("Please choose your product category: \n\n" + 
                    "/general" + "\n" + 
                    "/books" + "\n" + 
                    "/electronics" + "\n" + 
                    "/food")
        update.message.reply_text(response)

    # Initiates model for general product category 
    def general(self, update, context):
        if self.is_logged_in(update):
            self.wait(update)
            chat_id = update.message.chat_id
            current_users[chat_id]["model"] = "general"
            print(f"Current users: {current_users}")
            username = current_users[chat_id]["email"]
            url = storage.child(f"{username}/Reviews.csv").get_url(None)
            print("loading model...")
            self.models[chat_id] = Distilbert(url, "general")
            self.choose_function(update)
        else:
            response = "You are currently not logged in, please log in! \n\n/login"
            update.message.reply_text(response)

    # Initiates model for books product category 
    def books(self, update, context):
        if self.is_logged_in(update):
            self.wait(update)
            chat_id = update.message.chat_id
            current_users[chat_id]["model"] = "books"
            print(f"Current users: {current_users}")
            username = current_users[chat_id]["email"]
            url = storage.child(f"{username}/Reviews.csv").get_url(None)
            print("loading model...")
            self.models[chat_id] = Distilbert(url, "books")
            self.choose_function(update)
        else:
            response = "You are currently not logged in, please log in! \n\n/login"
            update.message.reply_text(response)
    
    # Initiates model for electronics product category 
    def electronics(self, update, context):
        if self.is_logged_in(update):
            self.wait(update)
            chat_id = update.message.chat_id
            current_users[chat_id]["model"] = "electronics"
            print(f"Current users: {current_users}")
            username = current_users[chat_id]["email"]
            url = storage.child(f"{username}/Reviews.csv").get_url(None)
            print("loading model...")
            self.models[chat_id] = Distilbert(url, "electronics")
            self.choose_function(update)
        else:
            response = "You are currently not logged in, please log in! \n\n/login"
            update.message.reply_text(response)
    
    # Initiates model for food product category 
    def food(self, update, context):
        if self.is_logged_in(update):
            self.wait(update)
            chat_id = update.message.chat_id
            current_users[chat_id]["model"] = "food"
            print(f"Current users: {current_users}")
            username = current_users[chat_id]["email"]
            url = storage.child(f"{username}/Reviews.csv").get_url(None)
            print("loading model...")
            self.models[chat_id] = Distilbert(url, "food")
            self.choose_function(update)
        else:
            response = "You are currently not logged in, please log in! \n\n/login"
            update.message.reply_text(response)

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
        if self.is_logged_in(update):
            response = "Please send the new set of reviews"
            update.message.reply_text(response)
        else:
            response = "You are currently not logged in, please log in! \n\n/login"
            update.message.reply_text(response)

    # Check if downloaded document is in correct format
    def is_correct_format(self, document):
        file_path = document["file_path"]
        try:
            if is_csv(document):
                df = pd.read_csv(file_path)
                return "Reviews" in df.columns.values.tolist()
            elif is_xlsx(document):
                df = pd.read_excel(file_path)
                return "Reviews" in df.columns.values.tolist()
        except Exception as e:
            print(e)
            
    # Handles all document inputs
    def handle_document(self, update, context):
        if self.is_logged_in(update):
            document = context.bot.get_file(update.message.document)
            self.wait(update)
            if is_csv(document):
                try:
                    if self.is_correct_format(document):
                        chat_id = update.message.chat_id
                        if chat_id in current_users.keys():
                            username = current_users[chat_id]["email"]
                            print(f"username: {username}")
                            upload_csv(document, username)
                            response = "File received! Thank you for waiting patiently!"
                            update.message.reply_text(response)
                            self.choose_catgeory(update)
                        else:
                            response = "You have not logged in! Please log in first!\n\n/login"
                            update.message.reply_text(response)
                    else:
                        response = "File is not in correct format! Please make sure that the file has a column name 'Reviews' !"
                        update.message.reply_text(response)
                    
                except FileNotFoundError:
                    response = "File not received. Please try again!"
                    update.message.reply_text(response)
            elif is_xlsx(document):
                try:
                    if self.is_correct_format(document):
                        chat_id = update.message.chat_id
                        if chat_id in current_users.keys():
                            username = current_users[chat_id]["email"]
                            print(f"username: {username}")
                            upload_csv(document, username)
                            response = "File received! Thank you for waiting patiently!"
                            update.message.reply_text(response)
                            self.choose_catgeory(update)
                        else:
                            response = "You have not logged in! Please log in first!\n\n/login"
                            update.message.reply_text(response)
                    else:
                        response = "File is not in correct format! Please make sure that the file has a column name 'Reviews' !"
                        update.message.reply_text(response)
                    
                except FileNotFoundError:
                    response = "File not received. Please try again!"
                    update.message.reply_text(response)
            else:
                response = "File not received. Please ensure that the file is in .csv or .xlsx!"
                update.message.reply_text(response)
        else:
            response = "You are currently not logged in, please log in! \n\n/login"
            update.message.reply_text(response)
