import sys
import os

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 将当前目录添加到Python的搜索路径中
sys.path.insert(0, current_dir)




import socket
from api import create_app
from pathlib import Path
import yaml
from config.config import config as _config

class ConfigMap(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

config = ConfigMap()
for k, v in _config.items():
    config[k] = v


app = create_app(config)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.get("PORT",5559), debug=config.get("DEBUG", False))
