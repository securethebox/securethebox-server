import sys


def writeConfig(**kwargs):
    template = """
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: cchong.vise@gmail.com
              """

    with open('./kubernetes-deployments/ingress/'+str(sys.argv[2])+'/01_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-permissions.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]), serviceName=str(sys.argv[2]))