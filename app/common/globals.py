global_vars = {
    "new_zipping_pathlib": []
}

def get_var(var_name):
    return global_vars.get(var_name)

def set_var(var_name, value):
    global_vars[var_name] = value