from pymongo import MongoClient

client = MongoClient('mongo', 27017)
question_answer_collection = client['PollApp']['QuestionAnswer']
