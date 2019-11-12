import sys

def writeConfig(**kwargs):
    template = """
kind: PersistentVolume
apiVersion: v1
metadata:
  name: {clusterName}-{serviceName}-{userName}-pv
  labels:
    type: local
  annotations:
    pv.beta.kubernetes.io/gid: "{gid}"
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/var/log/challenge{challengeId}"
              """

    with open('./kubernetes-deployments/storage/challenges/01_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-pv.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3],challengeId=int(),gid=int()))