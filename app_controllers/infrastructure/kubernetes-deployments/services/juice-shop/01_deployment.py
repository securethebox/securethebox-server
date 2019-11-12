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
        image: node:8-jessie
        ports:
          - containerPort: 3000
          - containerPort: 9000
        command: ["/bin/sh", "-c"]
        args:
        - git clone http://gitlab-{userName}/root/{serviceName}-{userName}.git &&
          cd {serviceName}-{userName} &&
          npm install &&
          npm run postinstall &&
          npm run start & 
          echo done ;
          while true ; do continue ; done ;
              """

    with open('./kubernetes-deployments/services/'+str(sys.argv[2])+'/01_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))