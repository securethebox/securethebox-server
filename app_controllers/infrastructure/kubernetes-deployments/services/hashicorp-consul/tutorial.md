ca-config.json 
{  
   "signing":{  
      "default":{  
         "expiry":"8760h"
      },
      "profiles":{  
         "default":{  
            "usages":[  
               "signing",
               "key encipherment",
               "server auth",
               "client auth"
            ],
            "expiry":"8760h"
         }
      }
   }
}

ca-csr.json 
{  
   "hosts":[  
      "cluster.local"
   ],
   "key":{  
      "algo":"rsa",
      "size":2048
   },
   "names":[  
      {  
         "C":"US",
         "L":"Portland",
         "O":"Kubernetes",
         "OU":"CA",
         "ST":"Oregon"
      }
   ]
}


consul-csr.json 
{
   "CN":"server.dc1.cluster.local",
   "hosts":[
      "server.dc1.cluster.local",
      "127.0.0.1"
   ],
   "key":{
      "algo":"rsa",
      "size":2048
   },
   "names":[
      {
         "C":"US",
         "L":"Portland",
         "O":"Comnsul",
         "OU":"Consul",
         "ST":"Oregon"
      }
   ]
} 

cfssl gencert -initca ca-csr.json | cfssljson -bare ca