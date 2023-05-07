# devproject

A tool for working in VSCode's Dev Containers.

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

## 3. Running projects

### 3.1. On current deployment configuration

```bash
dev run project-name
```

### 3.2. On specified deployment configuration

```bash
dev run project-name --config conf-name
```

### 3.3. Using specified base image

```bash
dev run project-name --base-image python:3.9
```

After openning the folder, run `F1` + `Dev Containers: Reopen in Container`.

Note: if you are running via Slurm, you need to srun into at least one node on remote before running this command.

## 4. Opening folder

### 4.1. Default

```bash
dev open /project/path
```

### 4.2. On specified deployment configuration

```bash
dev open /project/path --config conf-name
```

## 5. Configure global settings

### 5.1. Install extensions

- ms-vscode-remote.remote-containers
- ms-toolsai.jupyter-keymap
- nicohlr.pycharm
- ms-vscode-remote.remote-ssh
- ms-vscode-remote.remote-ssh-edit
- ms-vscode.remote-server
- ms-vscode-remote.vscode-remote-extensionpack
- ms-vscode.remote-explorer

### 5.2. Configure settings

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
    "editor.fontSize": 17,
    "editor.fontWeight": "normal",
    "editor.rulers": [79],
    "explorer.excludeGitIgnore": true,
    "files.autoSave": "afterDelay",
    "files.watcherExclude": {"**/**/**/**/*": true},
    "remote.SSH.remotePlatform": {},
    "search.useGlobalIgnoreFiles": true,
    "terminal.integrated.enableMultiLinePasteWarning": false,
    "workbench.colorTheme": "Pycharm Original Theme",
    "workbench.editor.untitled.hint": "hidden",
    "[python]": {"editor.formatOnType": true}
}
```
