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
      containers:
      - name: {serviceName}-{userName}
        image: trion/jenkins-docker-client
        env:
          - name: JAVA_OPTS
            value: -Djenkins.install.runSetupWizard=false
          - name: JENKINS_USER
            value: jenkins
        ports:
          - containerPort: 8080
          - containerPort: 8443
          - containerPort: 50000
        volumeMounts:
          - name: dockersock
            mountPath: "/var/run/docker.sock"
          - name: jenkins-home
            mountPath: /var/jenkins_home
      volumes:
      - name: jenkins-home
        emptyDir: {{}}
      - name: dockersock
        hostPath:
          path: /var/run/docker.sock
              """

    with open('./kubernetes-deployments/services/'+str(sys.argv[2])+'/01_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))