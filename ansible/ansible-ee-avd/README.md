```
(ansible-workspace) vscode@b54008fea2db:/workspace/ansible/awx/avd-ee$ ansible-builder build --tag registry.idcfcloud.com/vds/ansible-ee-avd:latest --container-runtime docker
Running command:
  docker build -f context/Dockerfile -t registry.idcfcloud.com/vds/ansible-ee-avd:latest context
Complete! The build context can be found at: /workspace/ansible/awx/avd-ee/context
```
```
❯ docker push registry.idcfcloud.com/vds/ansible-ee-avd:latest
The push refers to repository [registry.idcfcloud.com/vds/ansible-ee-avd]
9041bae40b7d: Pushed
803f27a4e795: Pushed
5f70bf18a086: Pushed
f5db85d91124: Pushed
8e101b297f6f: Pushed
e4c74088179e: Pushed
d84fa6dca61c: Pushed
8457d108a399: Pushed
d5fc552fe0e6: Pushed
d441a97c20b3: Pushed
a221b7de98e0: Pushed
cf45781a6e52: Pushed
60cc49ceeebb: Pushed
e5639813d9bc: Pushed
17331470cdff: Pushed
latest: digest: sha256:e9b77eea953464a15e8da47a8928694ace7468f011a6d25e4b3af047d5c284ec size: 3459
```
