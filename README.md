# MinerU 集成镜像项目

将 [MinerU](https://github.com/opendatalab/MinerU) (v1.2.2) 打包为离线 Docker 整合方案。

## 功能特性

* 📦 集成 MinerU 1.2.2
* 🖥️ 内置 MinerU-WebDemo 可视化界面和离线swagger文档
* 🐳 开箱即用的 Docker 容器化部署，容器内已下好需要的所有模型
* 🔧 支持环境变量配置

## 快速开始

```bash
docker pull crpi-omrdia1j1e0m0x6k.cn-hangzhou.personal.cr.aliyuncs.com/chiayen/mineru-web:v1.2.2-fix
docker run -itd --gpus all -p 5559:5559 crpi-omrdia1j1e0m0x6k.cn-hangzhou.personal.cr.aliyuncs.com/chiayen/mineru-web:v1.2.2-fix
```

- 请求`http://localhost:5559` MinerU-WebUI 界面。
- 请求`http://localhost:5559/docs` 可访问 MinerU-WebUI 离线swagger文档。
- 请求`http://localhost:5559/openapi.json` 可获得 MinerU-WebUI Openapi.json。

### 环境变量说明

| 环境变量 | 描述                   | 默认值 | 
| --- |----------------------| --- | 
| DEBUG | 调试模式开关               | false |
| IP | 服务监听的IP地址            | localhost |
| PORT | 服务监听的端口号             | 5559 | 
| LOG_LEVEL | 日志级别                 | DEBUG | 
| SQLALCHEMY_TRACK_MODIFICATIONS | SQLAlchemy的追踪修改功能开关  | true |
| PROPAGATE_EXCEPTIONS | 异常传播功能开关             | true |
| PREFERRED_URL_SCHEME | 首选的URL协议             | http |
| SECRET_KEY | 应用的密钥，用于会话加密         | your_secret_key |
| JWT_SECRET_KEY | JWT的密钥，用于生成和验证JWT令牌  | your_jwt_secret_key |
| JWT_ACCESS_TOKEN_EXPIRES | JWT访问令牌的过期时间（秒）      | 3600 |
| PDF_UPLOAD_FOLDER | PDF文件上传的文件夹          | upload_pdf |
| PDF_ANALYSIS_FOLDER | PDF文件分析结果存储的文件夹      | analysis_pdf |
| REACT_APP_DIST | React应用的静态文件目录       | ./dist/ |
| FILE_API | 文件API的URL路径          | /api/v2/analysis/pdf_img?as_attachment=False |
| DATABASE_TYPE | 数据库类型，可选sqlite或mysql | sqlite |
| DATABASE_PATH | 数据库文件路径              | config/mineru_web.db |
| MYSQL_USER | MySQL数据库的用户名（可选）     | root |
| MYSQL_PASSWORD | MySQL数据库的密码（可选）      | password |
| MYSQL_HOST | MySQL数据库的主机地址（可选）    | localhost |
| MYSQL_PORT | MySQL数据库的端口号（可选）     | 3306 |
| MYSQL_DATABASE | MySQL数据库的名称（可选）      | mineru_web |

## 使用docker-compose启动

项目中提供了`docker-compose.yml`文件，使用`docker-compose up -d`命令即可启动。

## 感谢

本项目使用的webdemo来源于B站up易小灯塔的[一键整合包](https://www.bilibili.com/opus/998007995670462467?from=search&spm_id_from=333.337.0.0)，本人进行了配置文件的环境变量改造和内置api文档的开发。



