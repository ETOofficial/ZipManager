import datetime
import os

def getsize(path):
    file_size = os.path.getsize(path)
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
    
def getmtime(path):
    modification_time = os.path.getmtime(path)
    return datetime.datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
    
def getctime(path):
    creation_time = os.path.getctime(path)
    return datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')

def getatime(path):
    access_time = os.path.getatime(path)
    return datetime.datetime.fromtimestamp(access_time).strftime('%Y-%m-%d %H:%M:%S')

def getname(path):
    return os.path.basename(path)
def getinfo(path):
    return {
        'name': getname(path),
        'size': getsize(path),
        'mtime': getmtime(path),
        'ctime': getctime(path),
        'atime': getatime(path)
    }

def remove_nested(path_list):
    """移除嵌套的文件（夹）"""
    for i, path_i in enumerate(path_list[:-1]):
        for j, path_j in enumerate(path_list[i+1:]):
            if len(path_i) >= len(path_j):
                if path_i[:len(path_j)] == path_j:
                    path_list[i] = ""
            elif len(path_i) < len(path_j):
                if path_j[:len(path_i)] == path_i:
                    path_list[i+j+1] = ""
    path_list = [i for i in path_list if i != ""]
    return path_list