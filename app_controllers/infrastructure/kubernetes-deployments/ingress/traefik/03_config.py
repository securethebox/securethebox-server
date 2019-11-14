import sys

def writeConfig(**kwargs):
    template = """
kind: ConfigMap
apiVersion: v1
metadata:
  name: traefik-config
  namespace: default
data:
  traefik.toml: |
    defaultEntryPoints = ["http", "https"]
    [entryPoints]
      [entryPoints.http]
      address = ":80"
      #   [entryPoints.http.redirect]
      #     entryPoint = "https"
      # [entryPoints.https]
      # address = ":443"
      #   [entryPoints.https.tls]
    [kubernetes]
    [respondingTimeouts]
      # idleTimeout is the maximum duration an idle (keep-alive) connection will remain idle before closing itself.
      # This needs to be set longer than the GCP load balancer timeout
      idleTimeout = "620s"
              """

    with open('./kubernetes-deployments/ingress/'+str(sys.argv[2])+'/03_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-config.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))


if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]), serviceName=str(sys.argv[2]))