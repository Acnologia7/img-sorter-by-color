# Image sorter by average color

## Prequisities
### Docker
1. Make sure you have working Docker on your system
2. Some images

### Clone this repo
Use command ```git clone https://github.com/Acnologia7/img-sorter-by-color.git```

## Instalation
### 1. Prepare HOST directories
Make sure that you have prepared directory for inputs and outputs on your HOST system

###  2. Prepare .env file
You can copy this and edit paths to your liking. Also make sure you have it on same level as ```docker-compose.yml```
```
# NATS Configuration
NATS_PORT="4222"
NATS_SERVER_URL="nats://nats-server:4222" 

#Input and Output Directories
INPUT_BASE_DIRECTORY_HOST="Replace me with Absolute Path to your HOST directory for inputs(imgs)"
INPUT_BASE_DIRECTORY="Replace me with Absolute Path of GUEST directory tree to be binded for inputs (example: /inputs)"
OUTPUT_BASE_DIRECTORY_HOST="Replace me with Absolute Path to your HOST directory for outputs(imgs)"
OUTPUT_BASE_DIRECTORY="Replace me with Absolute Path of GUEST directory tree to be binded for outputs(example: /outputs)"

# Scan Interval
SCAN_INTERVAL="1"

# UI Configuration (concept example, not real UI)
SOURCE_INPUT_UI_DIRECTORY="Replace me with absolute Path to your HOST directory (and apend this: img-sorter-by-color/optional_ui/input)"
DESTINATION_INPUT_UI_DIRECTORY="Replace me with absolute Path to your HOST directory for inputs defined in INPUT_BASE_DIRECTORY_HOST (and append this: ui)
NATS_SERVER_LOCAL="nats://localhost:4222"
```

### 3. Build and start sorter
Run ```docker compose up``` command

### For "UI" example (not finished)
1. Make sure that there is directory ```input``` in ```optional_ui directory```
2. Make sure that paths are defined correctly
3. Put some image into optional_ui/input and name it "image.jpg"
4. Create venv, activate and install requirements.txt in optional_ui
4. Run main.py in ouptional_ui
