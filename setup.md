# Dev Container Setup

このリポジトリには Arista AVDのAnsible 開発用と Python 開発用の dev container が用意されています。
この手順書は、ローカルの VS Code から `Remote - SSH` で Linux ホストへ接続し、その接続先で dev container を起動する前提で記載しています。

実体は以下の構成です。

- `.devcontainer/ansible/devcontainer.json`
- `.devcontainer/python/devcontainer.json`
- `compose.yml`
- `ansible/Dockerfile`
- `ansible/postCreateCommand.sh`
- `python/Dockerfile`
- `python/postCreateCommand.sh`

## 対象の dev container

用途に応じて以下を使い分けます。

- Ansible 作業: `.devcontainer/ansible/devcontainer.json` と `compose.yml` の `ansible` サービス
- Python 作業: `.devcontainer/python/devcontainer.json` と `compose.yml` の `python` サービス

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

このワークスペースでは以下 2 つの dev container 定義が利用できます。

- Ansible 用: `.devcontainer/ansible/devcontainer.json`
- Python 用: `.devcontainer/python/devcontainer.json`

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

## 3. Remote - SSH 上で Dev Container を起動する

SSH 接続済みの VS Code ウィンドウでコマンドパレットを開き、次を実行します。

```text
Dev Containers: Reopen in Container
```

複数の定義があるため、表示された候補から用途に応じて以下を選択します。

- Ansible 作業を行う場合: `ansible`
- Python 作業を行う場合: `python`

初回起動時の流れは以下です。

1. SSH 接続先ホスト上の Docker が使われる
2. 選択した dev container に応じて `compose.yml` の `ansible` または `python` サービスが使われる
3. 対応する `ansible/Dockerfile` または `python/Dockerfile` からイメージがビルドされる
4. リポジトリ全体が `/workspace` にマウントされる
5. 対応する `ansible/postCreateCommand.sh` または `python/postCreateCommand.sh` が実行される

## 4. コンテナ内で何がセットアップされるか

### 共通セットアップ

`ansible/Dockerfile` と `python/Dockerfile` により、共通で主に以下がセットアップされます。

- Ubuntu 24.04 ベースの環境
- `uv` の導入
- `pyproject.toml` と `uv.lock` を使った Python 環境の同期
- `vscode` ユーザーの作成

また、`.devcontainer/ansible/devcontainer.json` と `.devcontainer/python/devcontainer.json` により以下も共通で追加されます。

- Docker outside of Docker
- Git
- SSHD
- Hadolint
- Aqua

### Ansible 用 dev container

`ansible/Dockerfile` により、追加で以下が実行されます。

- `requirements.yml` を使った Ansible Collection の導入

`ansible/postCreateCommand.sh` により以下が実行されます。

- `ansible/aqua.yaml` に定義された CLI ツールのインストール
- Python 仮想環境を使った `argcomplete` の有効化

さらに `.devcontainer/ansible/devcontainer.json` では以下が設定されます。

- 既定の Python インタープリタを `/app/.venv/bin/python` に設定
- Ansible 関連拡張の追加
- Ansible 向けの YAML ファイル関連付け

### Python 用 dev container

`python/postCreateCommand.sh` により以下が実行されます。

- `python/aqua.yaml` に定義された CLI ツールのインストール

さらに `.devcontainer/python/devcontainer.json` では以下が設定されます。

- 既定の Python インタープリタを `/app/.venv/bin/python` に設定
- `Ruff` と `Pylance` を前提にした Python 開発向け設定
- Python 関連拡張の追加

## 5. 動作確認

### Ansible 用 dev container の確認

コンテナ起動後、VS Code のターミナルで以下を実行してください。

```bash
cd /workspace/ansible
. envrc_common
task environment:check
```

`ANSIBLE_INVENTORY=./inventories/poc/hosts.ini` が必要なタスクは、`.envrc_poc` 読み込み後に実行してください。

実行例:

```bash
cd /workspace/ansible
. .envrc_poc
task playbook:info -- playbooks/sample.yml
```

### Python 用 dev container の確認

コンテナ起動後、VS Code のターミナルで以下を実行してください。

```bash
cd /workspace/python
. .envrc_common
task environment:check
```

Lint 実行例:

```bash
cd /workspace/python
task lint:run
```

## 補足

- ワークスペースはコンテナ内で `/workspace` にマウントされます
- Ansible 用 / Python 用のどちらでも Python インタープリタは `/app/.venv/bin/python` が使われます
- タイムゾーンは `Asia/Tokyo` に設定されています
- 既定ユーザーは `vscode` です
- Docker の実行主体はローカル PC ではなく SSH 接続先ホストです
