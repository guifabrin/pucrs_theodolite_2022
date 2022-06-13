helm install theodolite https://github.com/cau-se/theodolite/releases/download/v0.7.0/theodolite-0.7.0.tgz --kube-apiserver https://kubernetes.docker.internal:6443 --kube-ca-file ./cluster-ca-cert.pem --debug
sleep 60
helm test theodolite