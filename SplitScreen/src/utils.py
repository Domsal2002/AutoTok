import os

def create_directories():
    if not os.path.exists('videos'):
        os.makedirs('videos')
    if not os.path.exists('backgrounds'):
        os.makedirs('backgrounds')
