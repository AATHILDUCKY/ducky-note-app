# Ducky Notes App Automation Script

This repository contains a script to automate the setup and execution of the **Ducky Notes App**. The script ensures all dependencies, including `PyQt5`, are installed, activates a virtual environment, and runs the app effortlessly.

## Features

- **Automated Dependency Management**: Installs `PyQt5` if not already installed.
- **Virtual Environment Setup**: Automatically creates and activates a Python virtual environment.
- **System-Wide Access**: Allows running the app from any directory after moving the script to `/bin`.

## Installation and Usage

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### Step 2: Create the Executable Script

```bash
touch run_ducky_notes.sh
```

Open the file and paste the following script

```bash
#!/bin/bash

python /home/ducky/Desktop/ducky-note-app/ducky_notes.py"
```


### Step 3: Make the Script Executable

```bash
chmod +x run_ducky_notes.sh
```

### Step 4: Move the Script to ``/bin`` for System-Wide Access

1. Copy the script to ``/bin`` :
```bash
sudo cp run_ducky_notes.sh /bin/ducky_notes
```

2. Run the app from anywhere :
```bash
ducky_notes
```


## Usage

Once the setup is complete, you can run the Ducky Notes app from any location using the command