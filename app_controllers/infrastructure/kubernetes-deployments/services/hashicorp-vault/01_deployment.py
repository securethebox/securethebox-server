import sys

def writeConfig(**kwargs):
    template = """
kind: Deployment
apiVersion: extensions/v1beta1
metadata:
  name: {serviceName}-{userName}
  labels:
    app: {serviceName}-{userName}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {serviceName}-{userName}
  template:
    metadata:
      labels:
        app: {serviceName}-{userName}
    spec:
      volumes:
        - name: task-pv-storage
          persistentVolumeClaim:
            claimName: task-pv-claim
        - name: vault-config
          emptyDir: {{}}
        - name: vault-logs
          emptyDir: {{}}
        - name: vault-file
          emptyDir: {{}}
      containers:
      - name: {serviceName}-{userName}
        image: vault:latest
        ports:
        - containerPort: 8200
        securityContext:
          capabilities:
            add:
              - IPC_LOCK
        env:
          - name: VAULT_DEV_ROOT_TOKEN_ID
            value: "root"
        volumeMounts:
          - name: task-pv-storage
            mountPath: "/var/log/challenge1"
          - name: vault-config
            mountPath: "/vault/config"
          - name: vault-logs
            mountPath: "/vault/logs"
          - name: vault-file
            mountPath: "/vault/file"
              """

    with open('./kubernetes-deployments/services/'+str(sys.argv[2])+'/01_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))

# - name: VAULT_LOCAL_CONFIG
#             value: |
#               api_addr = "http://127.0.0.1"
#               log_level = "warn"
#               ui = true
#               listener "tcp" {
#                 address     = "127.0.0.1:8200"
#                 tls_disable = "true"
#               }
#               default_lease_ttl = 168h
#               max_lease_ttl = 720h
#               backend = {{file:{{\\"path\\":\\"/vault/file\"}}}}
# env:
# - name: VAULT_DEV_ROOT_TOKEN_ID
#   value: "root"

# - name: VAULT_LOCAL_CONFIG
#   value: "ui = true\nlistener \"tcp\" {\n address = \"0.0.0.0:8200\"\n tls_disable = 1\n}"

# export VAULT_ADDR=http://127.0.0.1:8200
# export VAULT_SKIP_VERIFY=true
# vault operator generate-root -init


# env:
# - name: VAULT_LOCAL_CONFIG
#   value: "{\"backend\": {\"file\": {\"path\": \"/vault/file\"}}, \"ui\":\"true\", \"default_lease_ttl\": \"168h\", \"max_lease_ttl\": \"720h\"}"