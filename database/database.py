"""
File that contains database information.
Here application tries to connect to MongoDB.
"""
import sys

from pymongo import MongoClient, errors

client = MongoClient('localhost', 27017, serverSelectionTimeoutMS=4000)
try:
    client.server_info()
except errors.ServerSelectionTimeoutError:
    try:
        client = MongoClient('mongo', 27017, serverSelectionTimeoutMS=4000)
    except errors.ServerSelectionTimeoutError:
        print("Could not connect to database. App will shut down.")
        sys.exit()

question_answer_collection = client['PollApp']['QuestionAnswer']
feedback_collection = client['FeedbackApp']['Feedback']
