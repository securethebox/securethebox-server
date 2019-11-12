import subprocess
from subprocess import check_output

def checkServiceOnline(clusterName,serviceName, userName):
    # Returns 'true' if service is online; 'false' if offline
    # make a get request, if it has the elements needed and the response is not 'service unavilable. return true
    print()
    

if __name__ == "__main__":
    checkServiceOnline('us-west1-a','jenkins','charles')