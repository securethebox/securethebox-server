# THIS SCRIPT SHOULD BE RUN ON CONSUL SERVER

# Use consul image:
# golang:1.11-alpine
# consul

# install golang 1.11
# install cfssl https://github.com/cloudflare/cfssl

go get -u github.com/cloudflare/cfssl/cmd/cfssl
go get -u github.com/cloudflare/cfssl/cmd/cfssljson
go get -u github.com/cloudflare/cfssl/cmd/...

# copy over files: ca-config.json, ca-key.json, consul-csr.json

cfssl gencert -initca ca-csr.json | cfssljson -bare ca

GOSSIP_ENCRYPTION_KEY=$(consul keygen)

cfssl gencert \
  -ca=ca.pem \
  -ca-key=ca-key.pem \
  -config=ca-config.json \
  -profile=default \
  consul-csr.json | cfssljson -bare consul

# Files created:
# ca-key.pem
# ca.pem
# ca.csr
# consul-key.pem
# consul.pem
# consul.csr

