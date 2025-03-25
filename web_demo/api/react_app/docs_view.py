from flask import render_template, Response, request,current_app
from flask_restful import Resource
import json


class SwaggerUIView(Resource):
    def get(self):
        swagger_html = render_template('/swagger-ui/index.html')
        return Response(swagger_html, mimetype='text/html')

class OpenAPIView(Resource):
    def get(self):
        openapi_json_path = current_app.config['REACT_APP_DIST']

        # 这里假设您的 openapi.json 存放在项目根目录
        with open(f'{openapi_json_path}/openapi.json', 'r') as f:
            data = json.load(f)
        data['host'] = request.host  # 动态设置host
        return Response(json.dumps(data), mimetype='application/json')
