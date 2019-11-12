import sys

def writeConfig(**kwargs):
    template = """
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: {clusterName}-{serviceName}-{userName}-pvc
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
              """

    with open('./kubernetes-deployments/storage/challenges/01_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-pvc.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))