import pyrebase

firebaseConfig={
    'apiKey': "AIzaSyBFDBNlmJUd2c61uCNVjnLmmz3ZagZ_2nM",
    'authDomain': "reviewo-43603.firebaseapp.com",
    'databaseURL': "https://reviewo-43603.firebaseio.com",
    'projectId': "reviewo-43603",
    'storageBucket': "reviewo-43603.appspot.com",
    'messagingSenderId': "988618292725",
    'appId': "1:988618292725:web:9f9e3d3b2a568d32e3f4bc",
    'measurementId': "G-HPL4M9T18H"
}

firebase = pyrebase.initialize_app(firebaseConfig)
# db=firebase.database()
storage = firebase.storage()
auth = firebase.auth()


# email = "zychin0@hotmail.com"
# password = "123456"
# cfm_password = "123456"

# if password == cfm_password:
#     try:
#         auth.create_user_with_email_and_password(email, password)
#         print("success!")
#     except Exception as e:
#         print(e)
# import urllib
# url = storage.child("UserGuide/test.xlsx").download("", "test.xlsx")
# print(url)
# with urllib.request.urlopen(url) as response_file:
#             print("Success")

# url = storage.child("zyfoodandtravel@gmail.com/Reviews.csv").get_url(None)
# df = pd.read_csv(url)
# print(df.head())