# the_guide

# Installation

Install Kubectl
```
brew install kubectl
```

Install Kustomize
```
brew install kustomize
```

Install  kustomize-sops-rs
```
curl -sL https://github.com/jaysonsantos/kustomize-sops-rs/raw/main/install.sh | bash -s
```

Install KSOPS
https://github.com/viaduct-ai/kustomize-sops

```
echo "export XDG_CONFIG_HOME=\$HOME/.config" >> $HOME/.bashrc
source $HOME/.bashrc
# Verify the $XDG_CONFIG_HOME environment variable exists then run
source <(curl -s https://raw.githubusercontent.com/viaduct-ai/kustomize-sops/master/scripts/install-ksops-archive.sh)

```
# Uses sops & 

# gitops config
Uses flux for gitops. Config steps:

```
flux bootstrap github \
  --owner=grai-io\
  --repository=the_guide \
  --branch=<organization default branch> \
  --team=<team1-slug> \
  --team=<team2-slug> \
  --path=./clusters/my-cluster
```