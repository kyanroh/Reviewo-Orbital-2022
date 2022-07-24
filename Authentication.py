from telegram.ext import Filters, ConversationHandler, CallbackContext, CommandHandler, MessageHandler
from database import auth
import os
import shutil

current_users = {}
'''{
    chat_id : {
        'email' : email,
        'password' : password
    }
}'''

class Signup:
    def __init__(self):
        self.ASK_EMAIL = 0
        self.GET_EMAIL_ASK_PASSWORD = 1
        self.GET_PASSWORD_ASK_CFM_PASSWORD = 2
        self.GET_CFM_PASSWORD_CHECK_LOGIN = 3
        self.convo_handler = ConversationHandler(
                                entry_points=[CommandHandler('signup', self.ask_email)],
                                states={
                                    self.ASK_EMAIL: [MessageHandler(Filters.text, callback=self.ask_email)],
                                    self.GET_EMAIL_ASK_PASSWORD: [MessageHandler(Filters.text, callback=self.get_email_ask_password)],
                                    self.GET_PASSWORD_ASK_CFM_PASSWORD: [MessageHandler(Filters.text, callback=self.get_password_ask_cfm_password)],
                                    self.GET_CFM_PASSWORD_CHECK_LOGIN: [MessageHandler(Filters.text, callback=self.get_cfm_password_check_login)],
                                },
                                fallbacks=[CommandHandler('quit', self.quit)]
                            )

    def ask_email(self, update, context):
        response = "Please enter your email"
        update.message.reply_text(response)
        return self.GET_EMAIL_ASK_PASSWORD

    def get_email_ask_password(self, update, context):
        email = update.message.text
        chat_id = update.message.chat_id
        if chat_id not in current_users.keys():
            current_users[chat_id] = {"email": email}
        else:
            current_users[chat_id]["email"] = email
        response = "Please enter your password"
        update.message.reply_text(response)
        return self.GET_PASSWORD_ASK_CFM_PASSWORD

    def get_password_ask_cfm_password(self, update, context):
        password = update.message.text
        chat_id = update.message.chat_id
        current_users[chat_id]['password'] = password
        response = "Please enter your password again"
        update.message.reply_text(response)
        return self.GET_CFM_PASSWORD_CHECK_LOGIN

    
    def get_cfm_password_check_login(self, update, context):
        chat_id = update.message.chat_id
        cfm_password = update.message.text
        if cfm_password == current_users[chat_id]['password']:
            chat_id = update.message.chat_id
            try:
                auth.create_user_with_email_and_password(current_users[chat_id]['email'], current_users[chat_id]['password'])
                self.make_path(current_users[chat_id]['email'])
            except Exception as e:
                print(e)
                del current_users[chat_id]
                response = "Email already exists! Please enter your email again!"
                update.message.reply_text(response)
                return self.GET_EMAIL_ASK_PASSWORD

            response = (f"Created account successfully! You are now logged in as {current_users[chat_id]['email']}!" + 
                            "Please send the input files for Customer Sentiment Analysis in a CSV or XLSX file")
            update.message.reply_text(response)
            print(f"Current users: {current_users}")
            return ConversationHandler.END
        else:
            del current_users[chat_id]
            response = "Passwords are not the same! Please enter your email again!"
            update.message.reply_text(response)
            return self.GET_EMAIL_ASK_PASSWORD 

    def quit(self):
         return ConversationHandler.END
    
    def make_path(self, name):
        new_path = os.path.dirname(__file__) + f"/{name}"
        if not os.path.exists(new_path):
            os.makedirs(new_path)

class Login:
    def __init__(self):
        self.CHECK_LOGIN_STATUS = 0
        self.ASK_EMAIL = 1
        self.GET_EMAIL_ASK_PASSWORD = 2
        self.GET_PASSWORD_CHECK_LOGIN = 3
        self.convo_handler = ConversationHandler(
                                entry_points=[CommandHandler('login', self.check_login_status)],
                                states={
                                    self.ASK_EMAIL: [MessageHandler(Filters.text, callback=self.ask_email)],
                                    self.GET_EMAIL_ASK_PASSWORD: [MessageHandler(Filters.text, callback=self.get_email_ask_password)],
                                    self.GET_PASSWORD_CHECK_LOGIN: [MessageHandler(Filters.text, callback=self.get_password_check_login)],
                                },
                                fallbacks=[CommandHandler('quit', self.quit)]
                            )
    
    def is_logged_in(self, update):
        chat_id = update.message.chat_id
        return chat_id in current_users.keys()

    def check_login_status(self, update, context):
        chat_id = update.message.chat_id
        if self.is_logged_in(update):
            response = f"You are already logged in as {current_users[chat_id]['email']}! Please logout first before you login to another account! \n\n/logout"
            update.message.reply_text(response)
            return ConversationHandler.END
        else:
            next_state = self.ask_email(update, context)
            return next_state

    def ask_email(self, update, context):
        response = "Please enter your email"
        update.message.reply_text(response)
        return self.GET_EMAIL_ASK_PASSWORD

    def get_email_ask_password(self, update, context):
        email = update.message.text
        chat_id = update.message.chat_id
        if chat_id not in current_users.keys():
            current_users[chat_id] = {"email": email}
        else:
            current_users[chat_id]["email"] = email
        response = "Please enter your password"
        update.message.reply_text(response)
        return self.GET_PASSWORD_CHECK_LOGIN
    
    def get_password_check_login(self, update, context):
        password = update.message.text
        chat_id = update.message.chat_id
        current_users[chat_id]["password"] = password

        try:
            auth.sign_in_with_email_and_password(current_users[chat_id]["email"], current_users[chat_id]["password"])
            # current_users[chat_id]["login_status"] = True
            response = (f"Login Successful! You are now logged in as {current_users[chat_id]['email']}!" + 
                            "\nPlease send the input files for Customer Sentiment Analysis in a CSV or XLSX file" + "\n\n" + 
                            "/delete_account")
            print(f"{current_users[chat_id]['email']} logged in!")
            print(f"Current users: {current_users}")
            update.message.reply_text(response)

            if not os.path.isdir(current_users[chat_id]['email']):
                self.make_path(current_users[chat_id]['email'])

            return ConversationHandler.END
        except Exception as e:
            print(e)
            response = "Invalid email or password. Please try again!\n\n/login"
            update.message.reply_text(response)
            del current_users[chat_id]
            # if chat_id not in current_users.keys():
            #     current_users[chat_id] = {"login_status": False}
            # else:
            #     current_users[chat_id]["login_status"] = False
            return ConversationHandler.END

    def make_path(self, name):
        new_path = os.path.dirname(__file__) + f"/{name}"
        if not os.path.exists(new_path):
            os.makedirs(new_path)

    def quit(self):
         return ConversationHandler.END

class Logout:
    def __init__(self):
        pass

    def logout(self, update, context):
        chat_id = update.message.chat_id
        print(f"{current_users[chat_id]['email']} logging out...")
        del current_users[chat_id]
        print(f"Current users: {current_users}")
        response = ("You have logged out successfully! Thank you for using our service! \n\n" + 
                    "/login\n" + 
                    "/signup\n" + 
                    "/about\n" + 
                    "/help")
        update.message.reply_text(response)

class DeleteCurrentAccount:
    def __init__(self):
        self.ASK_PASSWORD = 0
        self.GET_PASSWORD_DELETE_ACCOUNT = 1
        self.convo_handler = ConversationHandler(
                                entry_points=[CommandHandler('delete_account', self.check_login_status)],
                                states={
                                    self.ASK_PASSWORD : [MessageHandler(Filters.text, callback=self.ask_password)],
                                    self.GET_PASSWORD_DELETE_ACCOUNT: [MessageHandler(Filters.text, callback=self.get_password_delete_account)],
                                    },
                                fallbacks=[CommandHandler('quit', self.quit)]
                            )

    def is_logged_in(self, update):
        chat_id = update.message.chat_id
        if chat_id not in current_users.keys():
            response = "You are currently not logged in, please log in! \n\n/login"
            update.message.reply_text(response)
            return False
        else:
            return True

    def check_login_status(self, update, context):
        if self.is_logged_in(update):
            return self.ASK_PASSWORD
        else:
            return ConversationHandler.END

    def ask_password(self, update, context):
        response = "Please enter your password!"
        update.message.reply_text(response)
        return self.GET_PASSWORD_DELETE_ACCOUNT

    def get_password_delete_account(self, update, context):
        chat_id = update.message.chat_id
        password = update.message.text
        if password == current_users[chat_id]["password"]:
            print(f"Deleting account for {current_users[chat_id]['email']}")
            shutil.rmtree(current_users[chat_id]["email"])
            del current_users[chat_id]
            print(f"Current users: {current_users}")
            response = (f"You have deleted your account '{current_users[chat_id]['email']}' successfully! Thank you for using our service! \n\n" + 
                        "/login\n" + 
                        "/signup\n" + 
                        "/about\n" + 
                        "/help")
            update.message.reply_text(response)
            return ConversationHandler.END
        else:
            response = "Wrong password! Failed to delete account!"
            update.message_reply_text(response)
            return ConversationHandler.END

    def quit(self):
        return ConversationHandler.END

