import os

def get_all_routes():
    ret = []
    for dir in os.listdir('./routes/'):
        if '.py' in dir and '__' not in dir and 'f_' in dir:
            ret.append(dir.replace('.py', ''))
    return ret
