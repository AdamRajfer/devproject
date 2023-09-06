# devproject

Tools for working in VSCode.

## 1. Installation

```bash
pip install git+https://github.com/AdamRajfer/devproject
```

## 2. Deployment configuration

### 2.1. Local

```bash
dev config conf-name
```

### 2.2. Remote

```bash
dev config conf-name --gateway host-name
```

### 2.3. Remote via Slurm

```bash
dev config conf-name --gateway host-name --sync-host
```

### 2.4. Specified deployment path

```bash
dev config conf-name --deployment-path /deployment/path
```

### 2.5. Listing configurations

```bash
dev configs
```

The currently active configuration will be highlighted in green.

### 2.6. Removing existing cofiguration

```bash
dev config conf-name --rm
```

### 2.7. Changing the active configuration

```bash
dev config conf-name
```

## 3. Exploring directory

### 3.1. Default

```bash
dev explore /project/path
```

### 3.2. On specified deployment configuration

```bash
dev explore /project/path --config conf-name
```

## 4. Configure global settings

### 4.1. Install extensions

- ms-vscode-remote.remote-containers
- ms-toolsai.jupyter-keymap
- ms-vscode-remote.remote-ssh
- ms-vscode-remote.remote-ssh-edit
- ms-vscode.remote-server
- ms-vscode-remote.vscode-remote-extensionpack
- ms-vscode.remote-explorer

### 4.2. Configure settings

Run `F1` + `Prefereneces: Open User Settings (JSON)` and paste the following content to the file:

```json
{
    "audioCues.volume": 0,
    "dev.containers.defaultExtensions": [
        "eamodio.gitlens",
        "ms-azuretools.vscode-docker",
        "ms-python.black-formatter",
        "ms-python.isort",
        "ms-python.mypy-type-checker",
        "ms-python.python",
        "ms-toolsai.jupyter"
    ],
    "diffEditor.ignoreTrimWhitespace": false,
    "editor.accessibilitySupport": "on",
    "editor.rulers": [79],
    "explorer.excludeGitIgnore": true,
    "files.autoSave": "afterDelay",
    "search.useGlobalIgnoreFiles": true,
    "terminal.integrated.enableMultiLinePasteWarning": false,
    "workbench.editor.untitled.hint": "hidden",
    "[python]": {"editor.formatOnType": true}
}
```
