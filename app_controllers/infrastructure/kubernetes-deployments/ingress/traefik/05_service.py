import sys


def writeConfig(**kwargs):
    template = """
kind: Service
apiVersion: v1
metadata:
  name: {serviceName}-{clusterName}-ingress-controller
  annotations:
    external-dns.alpha.kubernetes.io/hostname: {serviceName}.{clusterName}.securethebox.us
spec:
  selector:
    app: {serviceName}-{clusterName}-ingress-controller
  ports:
    - protocol: TCP
      port: 443
      name: https
    - protocol: TCP
      port: 80
      name: http
    - protocol: TCP
      port: 8080
      name: admin
  type: LoadBalancer
              """

    with open('./kubernetes-deployments/ingress/'+str(sys.argv[2])+'/05_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-service.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]))