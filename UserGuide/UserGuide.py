from requests import request
from database import storage
import pandas as pd

class UserGuide:
    def __init__(self, reviewo_bot):
        self.next_page = 0
        self.reviewo_bot = reviewo_bot

    def start_tutorial(self, update, context):
        self.return_page_one(update, context)
    
    def end_tutorial(self, update, context):
        self.reviewo_bot.start(update, context)

    def next(self, update, context):
        if self.next_page == 1:
            self.return_page_one(update, context)
        elif self.next_page == 2:
            self.return_page_two(update, context)
        elif self.next_page == 3:
            self.return_page_three(update, context)
        elif self.next_page == 4:
            self.return_page_four(update, context)
        elif self.next_page == 5:
            self.return_page_five(update, context)
        elif self.next_page == 6:
            self.return_page_six(update, context)
        elif self.next_page == 7:
            self.return_page_seven(update, context)
        elif self.next_page == 8:
            self.return_page_eight(update, context)
        
    def return_page_one(self, update, context):
        chat_id = update.message.chat_id
        response = ("Welcome to reviewO, This is a tutorial on how to use the reviewO bot. " + 
                    "Below is the test file that we will be using for this tutorial, you may download it to try it out for yourself later. " + 
                    "Press /next to continue")
        update.message.reply_text(response)
        storage.child("UserGuide/test.xlsx").download("",'test.xlsx')
        with open("test.xlsx", "rb") as response_file:
            context.bot.send_document(chat_id, response_file)
        # import urllib.request
        # response = requests.get(url)
        # print(type(response.content))
        # with open(response, "rb") as response_file:
        # with urllib.request.urlopen(url) as response_file:
        #     context.bot.send_document(chat_id, response_file)
        self.next_page = 2
        return response
    
    def return_page_two(self, update, context):
        response = ("Ensure the review file you want to upload is in the same format as the test file." +  
                    "After sending in your review file, choose the category that your reviews fall under for more accurate results. " +
                    "For general reviews, you can click on the 'general' option. \n\nPress /next to continue")
        update.message.reply_text(response)
        self.next_page = 3
        return response
    
    def return_page_three(self, update, context):
        response = ("After choosing your product category, many options will be available such as 'filter_fake_reviews', 'retrieve_predictions', 'sort_predicted_reviews', 'compile_top_five_words.' "
                    "We will go through all the options in this tutorial to have a full understanding of the functions of ReviewO. " + 
                    "Let's start with 'filter_fake_reviews'. \n\nPress /next  to continue")
        update.message.reply_text(response)
        self.next_page = 4
        return response

    def return_page_four(self, update, context):
        chat_id = update.message.chat_id
        response = ("Upon clicking 'filter_fake_reviews', ReviewO will automatically go through your reviews and remove any inputs that may have potentially been written by bots. " + 
                    "A new cleaned file will be returned. Take a look at the new test file that has been returned. " + 
                    "Notice that the first few repeated lines have been removed since it has been deemed as having been written by bots. " + 
                    "We can now reupload the new cleaned file for ReviewO to carry out the other functions. \n\nPress /next to continue")
        update.message.reply_text(response)
        storage.child("UserGuide/filtered_reviews.xlsx").download("",'filtered_reviews.xlsx')
        with open("filtered_reviews.xlsx", "rb") as response_file:
            context.bot.send_document(chat_id, response_file)
        # url = storage.child("UserGuide/filtered_reviews.xlsx").get_url(None)
        # with open(url, "rb") as response_file:
        #     context.bot.send_document(chat_id, response_file)
        self.next_page = 5
        return response

    def return_page_five(self, update, context):
        chat_id = update.message.chat_id
        response = ("Next we will look at the 'retrieve_predictions' feature. " + 
                    "ReviewO will return a new excel file containing 1 column of your reviews and a new column with the predicted sentiment beside it. " + 
                    "The sentiment column will come in the form “Negative” or “Positive”. \n\nPress /next to continue")
        update.message.reply_text(response)
        storage.child("UserGuide/predicted_reviews.xlsx").download("",'predicted_reviews.xlsx')
        with open("predicted_reviews.xlsx", "rb") as response_file:
            context.bot.send_document(chat_id, response_file)
        # url = storage.child("UserGuide/predicted_reviews.xlsx").get_url(None)
        # with open(url, "rb") as response_file:
        #     context.bot.send_document(chat_id, response_file)
        self.next_page = 6
        return response

    def return_page_six(self, update, context):
        chat_id = update.message.chat_id
        response = ("Next we will look at the 'sort_predicted_reviews' feature. ReviewO will help to sort the predicted reviews into 2 individual excel files. " +
                    "One of them contains all the positive sentiment reviews while the other contains the negative ones. " + 
                    "This feature will help Users such as shop owners easily understand the sentiments of satisfied and unsatisfied customers to see where they can improve or keep doing well. " + 
                    "\n\nPress /next to continue")
        update.message.reply_text(response)
        storage.child("UserGuide/good_reviews.xlsx").download("",'good_reviews.xlsx')
        with open("good_reviews.xlsx", "rb") as response_file:
            context.bot.send_document(chat_id, response_file)
        storage.child("UserGuide/bad_reviews.xlsx").download("",'bad_reviews.xlsx')
        with open("bad_reviews.xlsx", "rb") as response_file:
            context.bot.send_document(chat_id, response_file)
        # url = storage.child("UserGuide/good_reviews.xlsx").get_url(None)
        # with open(url, "rb") as response_file:
        #     context.bot.send_document(chat_id, response_file)
        # url = storage.child("UserGuide/bad_reviews.xlsx").get_url(None)
        # with open(url, "rb") as response_file:
        #     context.bot.send_document(chat_id, response_file)
        self.next_page = 7
        return response

    def return_page_seven(self, update, context):
        response = ("Next we will look at the 'compile_top_five_words' feature. " + 
                    "When clicked, ReviewO will send a short compiled list of the top 5 most common words that appear for each type of review. " + 
                    "For a total of 10 words, the top 5 words used in negative reviews and top 5 words used in positive reviews will be displayed in a text bubble. " + 
                    "ReviewO will automatically remove any stop words such as pronouns and prepositions to show more descriptive words used in the reviews. " + 
                    "\n\nPress /next to continue")
        update.message.reply_text(response)
        response = ("Positive:" + "\n\n" + 
                    "tablet" + "\n" + 
                    "use" + "\n" + 
                    "great" + "\n" + 
                    "love" + "\n" + 
                    "app" + "\n\n" + 
                    "Negative:" + "\n\n" + 
                    "not" + "\n" +
                    "product" + "\n" +
                    "bought" + "\n" +
                    "want" + "\n" +
                    "disappoint")
        update.message.reply_text(response)
        self.next_page = 8
        return response

    def return_page_eight(self, update, context):
        response = ("That's the end of the ReviewO tutorial! Do give it a try for yourself!! " + 
                    "Do ensure that your input data is the same as the test file in the tutorial (Column name as well). " + 
                    "Thanks for using ReviewO :) \n\nPress /end_tutorial to continue")
        update.message.reply_text(response)
        self.next_page = 1
        return response