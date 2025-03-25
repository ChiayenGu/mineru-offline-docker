import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def get_env(key, default=None, required=False):
    value = os.environ.get(key, default)
    if required and not value:
        raise ValueError(f"Environment variable {key} is required")
    return value

# 基本配置
def get_base_config():
    try:
        debug = get_env('DEBUG', 'false').lower() == 'true'
        ip = get_env('IP', 'localhost')
        port = int(get_env('PORT', '5559'))
        log_level = get_env('LOG_LEVEL', 'DEBUG')
        sqlalchemy_track_modifications = get_env('SQLALCHEMY_TRACK_MODIFICATIONS', 'true').lower() == 'true'
        propagate_exceptions = get_env('PROPAGATE_EXCEPTIONS', 'true').lower() == 'true'
        preferred_url_scheme = get_env('PREFERRED_URL_SCHEME', 'http')
        return {
            'DEBUG': debug,
            'PORT': port,
            'SERVER_NAME':f'{ip}:{port}',
            "APPLICATION_DIR": '/',
            'PREFERRED_URL_SCHEME': preferred_url_scheme,
            'LOG_LEVEL': log_level,
            'SQLALCHEMY_TRACK_MODIFICATIONS': sqlalchemy_track_modifications,
            'PROPAGATE_EXCEPTIONS': propagate_exceptions
        }
    except ValueError as e:
        print(f"Error parsing base configuration: {e}")
        raise

# 安全配置
def get_security_config():
    secret_key = get_env('SECRET_KEY', "your_secret_key", required=True)
    jwt_secret_key = get_env('JWT_SECRET_KEY', "your_jwt_secret_key", required=True)
    try:
        jwt_access_token_expires = int(get_env('JWT_ACCESS_TOKEN_EXPIRES', '3600'))
        return {
            'SECRET_KEY': secret_key,
            'JWT_SECRET_KEY': jwt_secret_key,
            'JWT_ACCESS_TOKEN_EXPIRES': jwt_access_token_expires
        }
    except ValueError as e:
        print(f"Error parsing JWT access token expires: {e}")
        raise

# 文件存储
def get_file_storage_config():
    pdf_upload_folder = get_env('PDF_UPLOAD_FOLDER', 'upload_pdf')
    pdf_analysis_folder = get_env('PDF_ANALYSIS_FOLDER', 'analysis_pdf')
    react_app_dist = Path(BASE_DIR).joinpath(get_env('REACT_APP_DIST', './dist/'))
    file_api = get_env('FILE_API', '/api/v2/analysis/pdf_img?as_attachment=False')
    return {
        'PDF_UPLOAD_FOLDER': pdf_upload_folder,
        'PDF_ANALYSIS_FOLDER': pdf_analysis_folder,
        'REACT_APP_DIST': react_app_dist,
        'FILE_API': file_api
    }

# 数据库配置
def get_database_config():
    database_type = get_env('DATABASE_TYPE', 'sqlite')
    if database_type == 'sqlite':
        sqlalchemy_database_uri = f"sqlite:///{BASE_DIR}/{get_env('DATABASE_PATH', 'config/mineru_web.db')}"
    elif database_type == 'mysql':
        sqlalchemy_database_uri = (
            f"mysql+pymysql://{get_env('MYSQL_USER', 'root', required=True)}"
            f":{get_env('MYSQL_PASSWORD', 'password', required=True)}"
            f"@{get_env('MYSQL_HOST', 'localhost', required=True)}"
            f":{get_env('MYSQL_PORT', '3306')}"
            f"/{get_env('MYSQL_DATABASE', 'mineru_web', required=True)}"
        )
    else:
        raise ValueError(f"Unsupported database type: {database_type}")
    return {
        'DATABASE_TYPE': database_type,
        'SQLALCHEMY_DATABASE_URI': sqlalchemy_database_uri
    }

# 合并所有配置
config = {
    **get_base_config(),
    **get_security_config(),
    **get_file_storage_config(),
    **get_database_config()
}
