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

def remove_nested(lst, isPathList=True, key="path"):
    """
    移除嵌套的文件（夹）
    
    :param lst: **路径列表** 或 **文件信息（字典）列表**
    :param isPathList: 如果 ``lst`` 是 **路径列表** 则为 ``True`` ，如果是 **文件信息列表** 则为 ``False`` 。不接受其他列表。
    :param key: 键名
    :returns: 处理过的列表
    """
    if isPathList:
        for i, path_i in enumerate(lst[:-1]):
            for j, path_j in enumerate(lst[i + 1:]):
                if len(path_i) >= len(path_j):
                    if path_i[:len(path_j)] == path_j:
                        lst[i] = ""
                elif len(path_i) < len(path_j):
                    if path_j[:len(path_i)] == path_i:
                        lst[i + j + 1] = ""
        lst = [i for i in lst if i != ""]
        return lst
    else:
        for i, path_i in enumerate(lst[:-1]):
            for j, path_j in enumerate(lst[i + 1:]):
                if len(path_i[key]) >= len(path_j[key]):
                    if path_i[key][:len(path_j[key])] == path_j[key]:
                        lst[i][key] = ""
                elif len(path_i[key]) < len(path_j[key]):
                    if path_j[key][:len(path_i[key])] == path_i[key]:
                        lst[i + j + 1][key] = ""
        lst = [i for i in lst if i[key] != ""]
        return lst
    
def dict_to_list(dic:dict, sort:list[str]):
    return [dic[i] for i in sort]

def dictList_to_listList(dicList:list[dict], sort:list[str]):
    """将字典列表转为列表列表，便于表格传参"""
    return [dict_to_list(i, sort) for i in dicList]