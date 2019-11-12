import datetime
import pprint

class Question(object):
    def __init__(self, qid, title, description):
        self.id = qid
        self.title = title
        self.description = description
        self.difficulty = 0 # easy, medium, hard
        self.upvotes = 0
        self.downvotes = 0
        self.attempts = 0
        self.companies = []
        self.tips = []
        self.solutions = []
        self.member_only = False

    def add_upvote(self):
        self.upvotes += 1

    def remove_upvote(self):
        self.upvotes -= 1

    def add_downvote(self):
        self.downvotes += 1
    
    def remove_downvote(self):
        self.downvotes -= 1

    def set_difficulty(self, difficulty_rating):
        self.difficulty = difficulty_rating
    
    def add_attempt(self):
        self.attempts += 1

    def add_company(self,company_name):
        self.companies.append(company_name)
    
    def add_tip(self, tip_description):
        self.tips.append(tip_description)

    def add_solution(self, solution_object):
        """
        type: ie. vocal, coding, video, definition
        test_cases = 0 - 100
        keywords = ['pki','kubernetes'] # search answer for words
        keyword_accuracy_threshold = 90%
        """
        self.solutions.append(solution_object)
