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
      containers:
      - name: {serviceName}-{userName}
        image: splunk/universalforwarder:latest
        ports:
        - containerPort: 9997
        env:
          - name: SPLUNK_START_ARGS
            value: --accept-license
          - name: SPLUNK_USER
            value: root
          - name: SPLUNK_PASSWORD
            value: Changeme
        volumeMounts:
        - mountPath: "/var/log/challenge1"
          name: task-pv-storage
              """

    with open('./kubernetes-deployments/services/'+str(sys.argv[2])+'/01_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))