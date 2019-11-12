class Solution(object):
    def __init__(self, sid, qid, solution_type, content):
        self.id = sid
        self.question_id = qid
        self.type = "text" # text, vocal, coding, video
        self.textbox = "" # markdown format of textbox
        self.reference_urls = [] # list of urls
        self.reference_attachments = [] # list of urls to files

    def edit_textbox(self, textbox):
        self.textbox = textbox
    
    def add_reference_url(self, url):
        self.reference_urls.append(url)

    def remove_reference_url(self, url):
        self.reference_urls.pop(url)

    def add_reference_attachments(self, attachment):
        self.reference_attachments.append(attachment)

    def remove_reference_attachments(self, attachment):
        self.reference_attachments.pop(attachment)

    def set_type(self, solution_type):
        self.type = solution_type