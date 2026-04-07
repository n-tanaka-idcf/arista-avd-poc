# Dev Container Setup

このリポジトリには Ansible 開発用の dev container が用意されています。
この手順書は、ローカルの VS Code から `Remote - SSH` で Linux ホストへ接続し、その接続先で dev container を起動する前提で記載しています。

実体は以下の構成です。

- `.devcontainer/ansible/devcontainer.json`
- `compose.yml`
- `ansible/Dockerfile`
- `ansible/postCreateCommand.sh`

## 前提条件

### ローカル PC 側

- Visual Studio Code
- VS Code 拡張 `Remote - SSH`
- VS Code 拡張 `Dev Containers`
- SSH クライアント

### SSH 接続先 Linux ホスト側

- Docker
- Docker Compose V2 (`docker compose` が使えること)
- Git
- このリポジトリが任意のディレクトリに clone 済みであること

確認例:

```bash
docker --version
docker compose version
git --version
```

## 1. Remote - SSH で接続する

ローカルの VS Code でコマンドパレットを開き、次を実行します。

```text
Remote-SSH: Connect to Host...
```

接続後、SSH 接続先ホスト上でこのリポジトリを開きます。

```text
File: Open Folder...
```

このワークスペースでは dev container 定義が `.devcontainer/ansible/devcontainer.json` にあります。

## 2. SSH 接続先でビルド用の `.env` を作成する

`compose.yml` ではビルド引数として `UID` と `GID` を使用します。
そのため、SSH 接続先ホストでリポジトリのルートに `.env` を作成します。

```bash
cat <<EOF > .env
UID=$(id -u)
GID=$(id -g)
EOF
```

この設定により、コンテナ内の `vscode` ユーザーと SSH 接続先ホストのユーザーの UID/GID をそろえやすくなります。

## 3. Remote SSH 上で Dev Container を起動する

SSH 接続済みの VS Code ウィンドウでコマンドパレットを開き、次を実行します。

```text
Dev Containers: Reopen in Container
```

初回起動時の流れは以下です。

1. SSH 接続先ホスト上の Docker が使われる
2. `compose.yml` の `ansible` サービスが使われる
3. `ansible/Dockerfile` からイメージがビルドされる
4. リポジトリ全体が `/workspace` にマウントされる
5. `postCreateCommand.sh` が実行される

## 4. コンテナ内で何がセットアップされるか

`ansible/Dockerfile` により、主に以下がセットアップされます。

- Ubuntu 24.04 ベースの環境
- `uv` の導入
- `pyproject.toml` と `uv.lock` を使った Python 環境の同期
- `requirements.yml` を使った Ansible Collection の導入
- `vscode` ユーザーの作成

また、`.devcontainer/ansible/devcontainer.json` により以下も追加されます。

- Docker outside of Docker
- Git
- SSHD
- Hadolint
- Aqua

さらに `ansible/postCreateCommand.sh` により以下が実行されます。

- `ansible/aqua.yaml` に定義された CLI ツールのインストール
- Python 仮想環境を使った `argcomplete` の有効化

## 5. 動作確認

コンテナ起動後、VS Code のターミナルで以下を実行してください。

```bash
cd /workspace/ansible
task environment:check
```

必要に応じて共通環境を読み込みます。

```bash
cd /workspace/ansible
. .envrc_common
```

POC inventory を使う場合は以下です。

```bash
cd /workspace/ansible
. .envrc_poc
```

`ANSIBLE_INVENTORY=./inventories/poc/hosts.ini` が必要なタスクは、`.envrc_poc` 読み込み後に実行してください。

実行例:

```bash
cd /workspace/ansible
. .envrc_poc
task playbook:info -- playbooks/sample.yml
```

## 6. SSH 接続先で手動ビルドする場合

dev container のベースとなるサービスは `compose.yml` で定義されています。
VS Code の `Reopen in Container` を使わずに確認したい場合は、SSH 接続先ホストでリポジトリルートから次を実行します。

```bash
docker compose build ansible
docker compose up -d ansible
docker compose exec ansible bash
```

コンテナに入った後の確認例:

```bash
cd /workspace/ansible
task environment:check
```

## 補足

- ワークスペースはコンテナ内で `/workspace` にマウントされます
- Ansible の Python インタープリタは `/app/.venv/bin/python` が使われます
- タイムゾーンは `Asia/Tokyo` に設定されています
- 既定ユーザーは `vscode` です
- Docker の実行主体はローカル PC ではなく SSH 接続先ホストです
