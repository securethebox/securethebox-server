#!/usr/bin/env python3

"""
Creates 'steps' within a 'challenge'
"""

from yattag import Doc

class Step(object):
    def __init__(self):
        doc, tag, text = Doc().tagtext()
        self.doc = doc
        self.tag = tag
        self.text = text
        self.bullet_list = []

    def add_title(self, title):
        # Header
        with self.tag('h1'):
            self.text(title)
        # Create a new line
        self.doc.stag('br')
        self.doc.stag('br')

    def add_item_to_bullet_list(self,item):
        self.bullet_list.append(item)

    def generate_bullet_list(self):
        with self.tag('ul'):
            for item in self.bullet_list:
                with self.tag('li'):
                    self.text(item)
    
    def add_block_of_text(self,some_text):
        with self.tag('p'):
            self.text(some_text)
        
    def print_html(self):
        print("doc:",self.doc.getvalue())
        return self.doc.getvalue()


this_step = Step()
this_step.add_title("test")
this_step.add_item_to_bullet_list('You receive alerts of an attack in progress against a web application from your SIEM (Splunk)')
this_step.add_item_to_bullet_list('The source of this alert if from the Web Application Firewall (Modsecurity)')
this_step.generate_bullet_list()
this_step.print_html()