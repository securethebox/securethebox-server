import sys

def writeConfig(**kwargs):
    template = """
kind: Deployment
apiVersion: extensions/v1beta1
metadata:
  name: {serviceName}-{clusterName}-ingress-controller
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: {serviceName}-{clusterName}-ingress-controller
    spec:
      serviceAccountName: {serviceName}-{clusterName}-ingress-controller
      terminationGracePeriodSeconds: 60
      volumes:
        - name: config
          configMap:
            name: traefik-config
      containers:
      - name: traefik
        image: "traefik:latest"
        volumeMounts:
          - mountPath: "/etc/traefik/config"
            name: config
        args:
        - --configfile=/etc/traefik/config/traefik.toml
        - --api
        - --kubernetes
        - --logLevel=DEBUG
              """

    with open('./kubernetes-deployments/ingress/'+str(sys.argv[2])+'/04_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]))