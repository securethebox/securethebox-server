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
        image: gitlab/gitlab-ce:latest
        ports:
          - containerPort: 80
          - containerPort: 443
          - containerPort: 8080
          - containerPort: 22
        volumeMounts:
          - name: dockersock
            mountPath: "/var/run/docker.sock"
          - name: gitlab-config
            mountPath: "/srv/gitlab/config"
          - name: gitlab-logs
            mountPath: "/srv/gitlab/logs"
          - name: gitlab-data
            mountPath: "/srv/gitlab/data"
      volumes:
      - name: gitlab-config
        hostPath:
          path: /etc/gitlab
      - name: gitlab-logs
        hostPath:
          path: /var/log/gitlab
      - name: gitlab-data
        hostPath:
          path: /var/opt/gitlab
      - name: dockersock
        hostPath:
          path: /var/run/docker.sock
              """

    with open('./kubernetes-deployments/services/'+str(sys.argv[2])+'/01_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))