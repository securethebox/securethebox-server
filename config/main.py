"""
Be sure to make files:
dev.json
prod.json
"""

import os

class AppEnv():
    def __init__(self):
        self.environment = ""
        self.config_file_path = ""

    def getHostEnvironment(self):
        current_environment = os.environ['APPENV']
        if current_environment == "DEV":
            print("APPENV environment variable is",current_environment)
            self.setHostEnvironment(current_environment)
            self.setConfigFilePath(os.getcwd()+"/dev.json")
            print(self.config_file_path)
            return current_environment
        elif current_environment == "PROD":
            print("APPENV environment variable is",current_environment)
            self.setHostEnvironment(current_environment)
            self.setConfigFilePath(os.getcwd()+"/prod.json")
            print(self.config_file_path)
            return current_environment
        else:
            print("APPENV environment variable not defined!")
            return current_environment

    def setHostEnvironment(self, env):
        self.environment = env

    def setConfigFilePath(self, filepath):
        self.config_file_path = filepath

    def getHostConfigFilePath(self):
        return self.config_file_path
    

if __name__ == "__main__":
    av = AppEnv()
    av.getHostEnvironment()