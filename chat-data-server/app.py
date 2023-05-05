from conf.config import DB_URI, OPENAI_KEY, OPENAI_MODEL
import re
from flask import Flask, request, Blueprint
import os
from flask_cors import CORS
from chatgpt import file_agent, read_data, sql_agent, api_key
import io
import contextlib
app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = OPENAI_KEY
CORS(app)

UPLOAD_FOLDER = f'{os.getcwd()}/upload_file'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')


@api_v1.route('/upload', methods=['POST'])
def upload_file():
    try:
        if request.method == 'POST':
            file = request.files['file']
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                df = read_data(f'{os.getcwd()}/upload_file/{filename}')
                df = df.fillna('')
                table_columns = df.columns.tolist()
                table_columns_el = [{'label': i, 'prop': i}
                                    for i in table_columns]
                table_datas_el = df.head(10).to_dict(orient='records')
                return {'code': '200', 'message': '文件上传成功', 'tableColumns': table_columns_el, 'tableData': table_datas_el}
            else:
                return {'code': '200', 'message': '文件上传失败'}
    except Exception as e:
        return {'code': '100', 'message': f'文件上传失败{str(e)}'}


def capture_output(func):
    def wrapper(*args, **kwargs):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            result = func(*args, **kwargs)
        output = buffer.getvalue()
        buffer.close()
        output = output.replace('\n', '<br>')
        output_str = re.sub(r'\u001b\[[^m]*m', '', output)
        return result, output_str
    return wrapper


@capture_output
def run_agent(agent, prompt):
    return agent.run(prompt)


@api_v1.route('/analytics', methods=['POST'])
def analystic_file():
    if request.method == 'POST':
        try:
            file_name = request.json.get('file_name')
            openai_api_key = request.json.get('openai_api_key')
            if openai_api_key:
                api_key(openai_api_key)
            if not file_name:
                raise Exception('请上传文件')
            prompt = request.json.get('prompt')
            if not prompt:
                raise Exception('请输入数据分析需求')
            agent = file_agent(f'./upload_file/{file_name}')
            result, output_str = run_agent(agent, prompt)
            return {'code': '200', 'message': result, 'thought': output_str}
        except Exception as e:
            return {'code': '100', 'message': f'{str(e)}'}
        finally:
            api_key(OPENAI_KEY)


@api_v1.route('/sql/analytics', methods=['POST'])
def analystic_sql():
    if request.method == 'POST':
        try:
            db_uri = request.json.get('db_uri')
            openai_api_key = request.json.get('openai_api_key')
            if openai_api_key:
                api_key(openai_api_key)
            if not db_uri:
                db_uri = DB_URI
                # raise Exception('请输入数据库连接')
            prompt = request.json.get('prompt')
            if not prompt:
                raise Exception('请输入数据分析需求')
            agent = sql_agent(db_uri)
            result, output_str = run_agent(agent, prompt)
            return {'code': '200', 'message': result, 'thought': output_str}
        except Exception as e:
            return {'code': '100', 'message': f'{str(e)}'}
        finally:
            api_key(OPENAI_KEY)


app.register_blueprint(api_v1)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
