import subprocess
import os
import requests
from lxml import html

def getResetToken():
    url = "http://gitlab-charles.us-west1-a.securethebox.us"
    headers = {
        'Host': "gitlab-charles.us-west1-a.securethebox.us"
        }
    response = requests.request("GET", url, headers=headers, allow_redirects=True)
    response_url = response.url
    password_token = response_url.split('=')
    print("PASSWORD TOKEN:",password_token[1])
    session_cookie = response.request.headers['Cookie']
    print("SESSION COOKIE:",response.request.headers['Cookie'])
    return password_token[1],session_cookie
    
def resetPasswordRequest(token,session):
    url = "http://gitlab-charles.us-west1-a.securethebox.us/users/password/edit?reset_password_token="+token
    headers = {
        'Host': "gitlab-charles.us-west1-a.securethebox.us",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie':session
        }
    page = requests.request("GET", url, headers=headers)
    tree = html.fromstring(page.content)
    authtoken = tree.xpath('//input[@name="authenticity_token"]')
    print("HEADERS:",headers)
    form_data = {
        "utf8": "✓",
        "_method": "put",
        "authenticity_token": authtoken[0].value,
        "user[reset_password_token]": token,
        "user[password]": "Changeme",
        "user[password_confirmation]": "Changeme",
    }
    submit_url = "http://gitlab-charles.us-west1-a.securethebox.us/users/password"
    print("FORM DATA:",form_data)
    submitform = requests.request("POST", submit_url, headers=headers, data=form_data)
    print("SUBMITTED STATUS CODE:",submitform.status_code)

def main():
    token,session = getResetToken()
    resetPasswordRequest(token,session)



if __name__ == "__main__":
    main()

    # http://gitlab-charles.us-west1-a.securethebox.us/users/password/edit?reset_password_token=dj-nykeSMJB5kSjKq4xu