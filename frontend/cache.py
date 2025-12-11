import os
import shutil

def create():
    # Create cache directory
    if not os.path.exists("cache"):
        os.mkdir("cache")

    # Create subdirectories
    for directory in ["docs", "chats", "summaries", "key-points", "risks", "additional-infos", "complicated-summaries"]:
        if not os.path.exists(f"cache/{directory}"):
            os.mkdir(f"cache/{directory}")
