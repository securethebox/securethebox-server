import datetime
import pprint

"""
'id'     : '0',
'title'  : 'Overview',
'content': '<h1>Overview</h1>' +
    '</br>This challenge assesses your skills in defending, responding, and preventing attacks against a web application.</li>' +
    '</br></br>'+
    '<ul>'+
    '<li>You will be graded on a Blue Team Incident Response scenario.</li>' +
    '<li>Time to complete this challenge is 2 hours.</li>' +
    '<li>Results will be emailed to you.</li>' +
    '<li>Candidates will demonstrate skill and experience with the following:</li><br/>'+
    '<ul>'+
    '<li>Linux CLI experience</li>'+
    '<li>Web Application Pentesting & Defense</li>'+
    '<li>Fullstack Development (Frontend/Backend/Database)</li>'+
    '<li>Scripting with bash/python/go/ruby/etc. </li>'+
    '<li>Reviewing code</li>'+
    '<li>Working with Web Application Firewalls</li>'+
    '<li>Analyzing log data with Splunk, ELK Stack, or classic Regular Expression techniques.</li>'+
    '<li>Experience with packet inspection</li>'+
    '<li>Creating YARA rules on Network/Host IDS/IPS</li>'+
    '<li>Experience with Operating System/Network Forensics</li>'+
    '</ul>'+
    '</ul>' +
    '<br/>' +   
    '</br>'
"""

class Challenge(object):
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.overview = ""
        self.date_published = datetime.datetime.now()
        self.last_update = datetime.datetime.now()
        self.change_history = {}
        self.difficulty = 0
        self.tags = []
        self.category = ""
        self.duration = 0
        self.grading_criteria = []
        self.apps = []
        self.topology = {}
        self.resources = {}
        self.questions = []
        self.submissions = {}

    def print_challenge(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.to_dict())

    def edit_title(self,new_title):
        self.title = new_title
    
    def edit_description(self,new_description):
        self.description = new_description

    def edit_overview(self,new_overview):
        self.overview = new_overview

    def edit_difficulty(self,new_difficulty):
        self.difficulty = int(new_difficulty)

    def add_tags(self, new_tag):
        if new_tag not in self.tags:
            self.tags.append(new_tag)
    
    def edit_category(self, new_category):
        self.category = new_category

    def edit_duration(self, new_duration):
        self.duration = new_duration

    def add_grading_criteria(self, new_criteria):
        if new_criteria not in self.grading_criteria:
            self.grading_criteria.append(new_criteria)

    def remove_grading_criteria(self, target_criteria):
        if target_criteria in self.grading_criteria:
            self.grading_criteria.remove(target_criteria)
    
    def add_app(self, new_app):
        if new_app not in self.apps:
            self.apps.append(new_app)

    def remove_app(self, target_app):
        if target_app in self.apps:
            self.apps.remove(target_app)
    
    def edit_topology(self, new_topology):
        self.topology = new_topology
    
    def add_resource(self, app_name, app_description, app_url, shell_url):
        self.resources[app_name] = {
                "description" : app_description,
                "app_url" : app_url, 
                "shell_url" : shell_url,
                "credentials" : {},
                "references" : [],
                "tips": []
            }

    # REFERENCES
    def add_resource_reference(self, resource_app_name, reference_title, 
                               reference_url):
        prev_resource = self.resources

        prev_resource[resource_app_name]["references"].append(
            {
                "title": reference_title,
                "url" : reference_url
            }
        )
        self.resources = prev_resource

    # def remove_resource_reference_by_index(self, target_resource_index):
    #     prev_resource = self.resources[target_resource_index]
    #     del prev_resource["references"][target_resource_index]
    #     self.resources = prev_resource

    # def remove_resource_by_index(self, target_index):
    #     del self.resources[target_index]

    # CREDENTIALS
    def add_resource_credential(self, resource_app_name, cred_user, 
                                 cred_password):
        prev_resource = self.resources[resource_app_name]
        prev_resource["credentials"] = {
            "user" : cred_user,
            "password" : cred_password
        }
        self.resources[resource_app_name] = prev_resource

    # def remove_resource_credential_by_index(self, target_resource_index):
    #     prev_resource = self.resources[target_resource_index]
    #     del prev_resource["credentials"][target_resource_index]
    #     self.resources = prev_resource

    # TIPS
    def add_resource_tip(self, resource_app_name, new_tip):
        prev_resource = self.resources[resource_app_name]
        prev_resource["tips"].append(new_tip)
        self.resources[resource_app_name] = prev_resource

    # def remove_resource_tip_by_index(self, target_resource_index):
    #     prev_resource = self.resources[target_resource_index]
    #     del prev_resource["credentials"][target_resource_index]
    #     self.resources = prev_resource

    # QUESTIONS
    def add_question(self,question_type, question_details):
        questions_size = len(self.questions)
        self.questions.append(
            {   
                "id" : questions_size,
                "type" : question_type,
                "details" : question_details
            }
        )

    # def edit_question_by_index(self,target_index,question_type, 
    #                            question_details):
    #     self.questions[target_index] = {
    #             "type" : question_type,
    #             "details" : question_details
    #         }

    # def remove_question_by_index(self, target_index):
    #     del self.questions[target_index]

    # SUBMISSIONS
    def add_submission(self, question_number, question_type, question_answer):
        self.submissions[question_number] = {
            "time" : datetime.datetime.now(),
            "type" : question_type,
            "answer" : question_answer
        }
    
    def edit_submission(self, target_submission_index, question_type, 
                        question_answer):
        self.submissions[target_submission_index] = {
            "time" : datetime.datetime.now(),
            "type" : question_type,
            "answer" : question_answer
        }

    # def remove_submission_by_index(self, target_submission_index):
    #     del self.submissions[target_submission_index]

    def save_challenge(self,author, timestamp, action):
        current_date = datetime.datetime.now()
        self.change_history[current_date] = {}
        change_history_current_date_size = len(self.change_history[current_date])
        self.change_history[current_date][change_history_current_date_size] = {
            "author" : author,
            "timestamp" : timestamp,
            "action" : action,
        }

    def to_dict(self):
        this_dict = {
            u'title':self.title,
            u'description':self.description,
            u'overview':self.overview,
            u'date_published':self.date_published,
            u'last_update':self.last_update,
            u'change_history':self.change_history,
            u'difficulty':self.difficulty,
            u'tags':self.tags,
            u'category':self.category,
            u'duration':self.duration,
            u'grading_criteria':self.grading_criteria,
            u'apps':self.apps,
            u'topology':self.topology,
            u'resources':self.resources,
            u'questions':self.questions,
            u'submissions':self.submissions,
        }

        return this_dict

    