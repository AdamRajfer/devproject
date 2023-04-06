# devproject

A tool for working in VSCode's Dev Containers.

## 1. Installation

```bash
pip install git+https://github.com/AdamRajfer/devproject
```

## 2. Deployment configuration

### 2.1. Local

```bash
dev config my-local-configuration
```

### 2.2. Remote

```bash
dev config my-remote-configuration --gateway my-host
```

### 2.3. Remote via Slurm

```bash
dev config my-remote-slurm-configuration --gateway my-host --sync-host
```

### 2.4. Specified deployment path

```bash
dev config my-configuration --deployment-path /path/to/my/deployment
```

### 2.5. Listing configurations

```bash
dev configs
```

The currently active configuration will be highlighted in green.

### 2.6. Removing existing cofiguration

```bash
dev config my-configuration-to-remove --rm
```

### 2.7. Changing the active configuration

```bash
dev config my-other-configuration
```

## 3. Creating projects

### 3.1. Default

```bash
dev project my-project
```

### 3.2. Specified base image

```bash
dev project my-project --base-image python:3.9
```

### 3.3. Specified workdir

```bash
dev project my-project --workdir relative/path/to/my/directory
```

### 3.4. Additional mounts

```bash
dev project my-project --mount source=/my/path/local,target=my/path/contaiener
```

### 3.5. Listing existing projects

```bash
dev projects
```

### 3.6. Removing existing project

```bash
dev project my-project-to-remove --rm
```

## 4. Running projects

### 4.1. On current deployment configuration

```bash
dev run my-project
```

### 4.2. On specified deployment configuration

```bash
dev run my-project --config my-deployment-configuration
```

After openning the folder, run `F1` + `Dev Containers: Reopen in Container`.

Note: if you are running via Slurm, you need to srun into at least one node on remote before running this command.

## 5. Opening folder

### 5.1. Default

```bash
dev open /my/folder/on/remote
```

### 5.2. On specified deployment configuration

```bash
dev open /my/folder/on/remote --config my-configuration
```

## 6. Configure global settings

### 6.1. Install extensions

- ms-vscode-remote.remote-containers
- ms-toolsai.jupyter-keymap
- nicohlr.pycharm
- ms-vscode-remote.remote-ssh
- ms-vscode-remote.remote-ssh-edit
- ms-vscode.remote-server
- ms-vscode-remote.vscode-remote-extensionpack
- ms-vscode.remote-explorer

### 6.2. Configure settings

Run `F1` + `Prefereneces: Open User Settings (JSON)` and paste the following content to the file:

```json
{
    "audioCues.volume": 0,
    "dev.containers.defaultExtensions": [
        "ms-python.python",
        "ms-python.isort",
        "ms-python.black-formatter",
        "ms-azuretools.vscode-docker",
        "matangover.mypy",
        "eamodio.gitlens"
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
