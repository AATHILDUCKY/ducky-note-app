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

# Define the virtual environment directory and Python script
ENV_DIR="env"
SCRIPT_PATH="/home/ducky/Desktop/ducky-note-app/ducky_notes.py"

# Function to check if PyQt is installed
check_and_install_pyqt() {
    # Activate the virtual environment
    source "$ENV_DIR/bin/activate"
    
    # Check if PyQt5 is installed
    if ! python -c "import PyQt5" &> /dev/null; then
        echo "PyQt5 not found. Installing..."
        pip install PyQt5
        
        # Check if the installation succeeded
        if python -c "import PyQt5" &> /dev/null; then
            echo "PyQt5 installed successfully."
        else
            echo "Failed to install PyQt5. Exiting..."
            deactivate
            exit 1
        fi
    else
        echo "PyQt5 is already installed."
    fi
}

# Ensure the virtual environment exists
if [ ! -d "$ENV_DIR" ]; then
    echo "Virtual environment not found. Creating one..."
    python -m venv "$ENV_DIR"
fi

# Check and install PyQt5
check_and_install_pyqt

# Run the Python script
echo "Running $SCRIPT_PATH..."
python "$SCRIPT_PATH"

# Deactivate the virtual environment
deactivate

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