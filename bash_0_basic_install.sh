grep certificate-authority-data ~/.kube/config  | awk '{ print $2 }' | base64 --decode > cluster-ca-cert.pem
sudo apt update && sudo apt-get install -y curl iptables
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm repo add theodolite https://cau-se.github.io/theodolite
helm repo update

git clone git@github.com:cau-se/theodolite.git