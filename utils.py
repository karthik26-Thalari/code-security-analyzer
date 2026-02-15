import time, os

IGNORED_DIRS = {".git", "node_modules", "__pycache__", "venv"}

class Timer:
    def __init__(self):
        self.t = time.time()
    def elapsed(self):
        return round(time.time() - self.t, 2)

def is_code_file(name):
    return name.endswith((".py",".js",".java",".c",".cpp"))

def walk_project(root):
    files = []
    for r,d,f in os.walk(root):
        d[:] = [x for x in d if x not in IGNORED_DIRS]
        for file in f:
            if is_code_file(file):
                files.append(os.path.join(r,file))
    return files
