import datetime
import os

def getsize(file_path):
    file_size = os.path.getsize(file_path)
    if file_size < 1024:
        return f"{file_size} B"
    elif file_size < 1024 ** 2:
        return f"{file_size / 1024:.2f} KB"
    elif file_size < 1024 ** 3:
        return f"{file_size / 1024** 2:.2f} MB"
    elif file_size < 1024 ** 4:
        return f"{file_size / 1024** 3:.2f} GB"
    else:
        return f"{file_size / 1024** 4:.2f} TB"
    
def getmtime(file_path):
    modification_time = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
    
def getctime(file_path):
    creation_time = os.path.getctime(file_path)
    return datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')

def getatime(file_path):
    access_time = os.path.getatime(file_path)
    return datetime.datetime.fromtimestamp(access_time).strftime('%Y-%m-%d %H:%M:%S')

def getname(file_path):
    return os.path.basename(file_path)
def getinfo(file_path):
    return {
        'name': getname(file_path),
        'size': getsize(file_path),
        'mtime': getmtime(file_path),
        'ctime': getctime(file_path),
        'atime': getatime(file_path)
    }