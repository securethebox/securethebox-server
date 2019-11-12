import requests
import json

def hashicorpVaultInitializeVaultGetRootTokenKeys():
    url1 = "http://localhost:8200/v1/sys/init"

    headers1 = {
        'Content-Type': 'application/json'
    }

    payload1 = "{\"secret_shares\":1,\"secret_threshold\":1}"
    response1 = requests.request("PUT",url1, data=payload1, headers=headers1)
    
    response_json = json.loads(response1.text)
    print("RESPONSE 1:",response_json['root_token'])
    root_token = response_json['root_token']
    key = response_json['keys'][0]
    print("KEY:",key)
    return root_token, key

def hashicorpVaultUnseal(key):
    url1 = "http://localhost:8200/v1/sys/unseal"

    headers1 = {
        'Content-Type': 'application/json'
    }

    payload1 = "{\"key\":"+key+",}"
    response1 = requests.request("PUT",url1, data=payload1, headers=headers1)
    response_json = json.loads(response1.text)
    print("Sealed Status:",response_json['sealed'])
    sealed_status = response_json['sealed']
    return sealed_status

def hashicorpVaultAuthenticateMethodToken(root_token):
    url1 = "http://localhost:8200/v1/auth/token/lookup-self"

    headers1 = {
        'Content-Type': 'application/json',
        'X-Vault-Token': root_token
    }

    response1 = requests.request("GET", url1, headers=headers1)
    print("RESPONSE 1:",response1.text)

if __name__ == "__main__":
    hashicorpVaultInitializeVaultGetRootTokenKeys()