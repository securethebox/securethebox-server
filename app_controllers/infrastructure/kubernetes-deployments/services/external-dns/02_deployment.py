import sys

def writeConfig(**kwargs):
    template = """
    apiVersion: extensions/v1beta1
    kind: Deployment
    metadata:
      name: external-dns
    spec:
      strategy:
        type: Recreate
      template:
        metadata:
          labels:
            app: external-dns
        spec:
          serviceAccountName: external-dns
          containers:
          - name: external-dns
            image: registry.opensource.zalan.do/teapot/external-dns:latest
            args:
            - --source=service
            - --source=ingress
            - --domain-filter={clusterName}.securethebox.us
            - --provider=google
            - --policy=upsert-only # would prevent ExternalDNS from deleting any records, omit to enable full synchronization
            - --registry=txt
            - --txt-owner-id=my-identifier
              """

    with open('02_external-dns-{clusterName}-deployment.yml', 'w') as yfile:
        yfile.write(template.format(**kwargs))

if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]))