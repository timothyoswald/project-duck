from pathlib import Path

# Get the folder this Python file is in
baseDir = Path(__file__).resolve().parent
# Path to the Images folder inside the project
imgDir = baseDir / "Images"
def getIMGpath(name):
    return str(imgDir / name)