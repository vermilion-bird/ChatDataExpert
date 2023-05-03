from flask import Flask, request, Blueprint
import os
from flask_cors import CORS
from chatgpt import file_agent,read_data,sql_agent
import io
import contextlib
app = Flask(__name__)
import os
import re
from conf.config import DB_URI,OPENAI_KEY
import os
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
                table_columns_el = [{'label':i,'prop':i} for i in table_columns]
                table_datas_el = df.head(10).to_dict(orient='records')
                return {'code':'200','message': '文件上传成功', 'tableColumns': table_columns_el,'tableData':table_datas_el}
            else:
                return {'code':'200', 'message': '文件上传失败'}
    except Exception as e:
        return {'code':'100', 'message': f'文件上传失败{str(e)}'}
  
        
@api_v1.route('/analytics', methods=['POST'])
def analystic_file():
    if request.method == 'POST':
        try:
            file_name = request.json.get('file_name')
            if not file_name:
                raise Exception('请上传文件')
            prompt = request.json.get('prompt')
            if not prompt:
                raise Exception('请输入数据分析需求')
            agent=file_agent(f'./upload_file/{file_name}')
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                result = agent.run(prompt)
            output = buffer.getvalue()
            buffer.close()
            #  将换行符替换为 <br> 标签       
            output=output.replace('\n','<br>')
            output_str = re.sub(r'\u001b\[[^m]*m', '', output)
            return {'code':'200', 'message': result, 'thought':output_str}
        except Exception as e:
            return {'code':'100', 'message': f'{str(e)}'}

@api_v1.route('/sql/analytics', methods=['POST'])
def analystic_sql():
    if request.method == 'POST':
        try:
            db_uri = request.json.get('db_uri')
            if not db_uri:
                db_uri = DB_URI
                # raise Exception('请输入数据库连接')
            prompt = request.json.get('prompt')
            if not prompt:
                raise Exception('请输入数据分析需求')
            agent=sql_agent(db_uri)
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                result = agent.run(prompt)
            output = buffer.getvalue()
            buffer.close()
            #将换行符替换为 <br> 标签       
            output=output.replace('\n','<br>')
            output_str = re.sub(r'\u001b\[[^m]*m', '', output)
            return {'code':'200', 'message': result, 'thought':output_str}
        except Exception as e:
            return {'code':'100', 'message': f'{str(e)}'}

app.register_blueprint(api_v1)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
