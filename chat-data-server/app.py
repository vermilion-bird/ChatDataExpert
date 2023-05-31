from conf.config import DB_URI, OPENAI_KEY, OPENAI_MODEL
import re
from flask import Flask, request, Blueprint, send_from_directory
import os
from flask_cors import CORS
from chatgpt import file_agent, read_data, sql_agent, create_llm, matplotlib_agent
import io
import contextlib
import time
from chatdoc import qa_with_doc
from langchain.document_loaders import PyPDFLoader,TextLoader,DirectoryLoader,Docx2txtLoader
from docment_process import doc_load
from chatgpt import es_embedding_text

app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = OPENAI_KEY
CORS(app)

UPLOAD_FOLDER = f'{os.getcwd()}/upload_file'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# def delete_file():

@api_v1.route('/list/dir', methods=['GET'])
def list_dir():
    try:
        project_name = request.args.get('project_name', type = str)
        project_path = f'{os.getcwd()}/documents/{project_name}'
        if not os.path.exists(project_path):
            raise Exception('项目不存在')
        return_files = []
        for root, dirs, files in os.walk(project_path):
            for name in files:
                file_path = os.path.join(root, name)
                if os.path.isfile(file_path):
                    file_type = name.split('.')[-1]
                    # 获取文件信息
                    file_info = os.stat(file_path)
                    # 文件大小
                    file_size = round(file_info.st_size / 1000 / 1000, 2)
                    # 文件创建时间
                    creation_time = file_info.st_ctime
                    return_files.append({'file_name': name, 'file_size': file_size, 'creation_time': time.ctime(creation_time), 'file_type': file_type})
        return {'code': 200, 'message': '文件列表获取成功', 'files': return_files}
    except Exception as e:
        return {'code': 100, 'message': f'文件列表获取失败{str(e)}'}

@api_v1.route('/create/project', methods=['GET'])
def create_project():
    try:
        project_name = request.args.get('project_name')
        if not project_name:
            raise Exception('请输入项目名称')
        if os.path.exists(f'{os.getcwd()}/documents/{project_name}'):
            raise Exception('请换个项目名称')
        project_path = f'{os.getcwd()}/documents/{project_name}'
        if not os.path.exists(project_path):
            os.makedirs(project_path)
        return {'code': 200, 'message': '项目创建成功'}
    except Exception as e:
        return {'code': 100, 'message': f'项目创建失败{str(e)}'}

@api_v1.route('/upload', methods=['POST'])
def upload_file():
    try:
        if request.method == 'POST':
            file = request.files['file']
            if file:
                file_type= request.form.get('file_type')
                project_name = request.form.get('project_name')
                filename = file.filename
                if file_type=='document':
                    # 文本类型文件
                    file_path = f'{os.getcwd()}/documents/{project_name}'
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    print(file_path)
                    file.save(f'{file_path}/{filename}')
                    file_full_path = f'{file_path}/{filename}'
                    docs = doc_load(file_full_path)
                    es_embedding_text(docs)
                    return {'code': 200, 'message': '文件上传成功'}
                else:
                    # 数据类型文件csv
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    df = read_data(f'{os.getcwd()}/upload_file/{filename}')
                    df = df.fillna('')
                    table_columns = df.columns.tolist()
                    table_columns_el = [{'label': i, 'prop': i}
                                        for i in table_columns]
                    table_datas_el = df.head(10).to_dict(orient='records')
                    return {'code': 200, 'message': '文件上传成功', 'tableColumns': table_columns_el, 'tableData': table_datas_el}
            else:
                return {'code': 200, 'message': '文件上传失败'}
    except Exception as e:
        return {'code': 100, 'message': f'文件上传失败,{str(e)}'}


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
                env_var(openai_api_key)
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
            env_var(OPENAI_KEY)

@api_v1.route('/matplotlib/analytics', methods=['POST'])
def analystic_matplotlib():
    if request.method == 'POST':
        try:
            file_name = request.json.get('file_name')
            openai_api_key = request.json.get('openai_api_key')
            if openai_api_key:
                env_var(openai_api_key)
            if not file_name:
                raise Exception('请上传文件')
            prompt = request.json.get('prompt')
            if not prompt:
                raise Exception('请输入数据分析需求')
            agent,plot_path = matplotlib_agent(f'./upload_file/{file_name}')
            result, output_str = run_agent(agent, prompt)
            plot_path = plot_path.replace('./temp','')
            return {'code': '200', 'message': result, 'thought': output_str, 'plot_path': plot_path}
        except Exception as e:
            return {'code': '100', 'message': f'{str(e)}'}
        finally:
            env_var(OPENAI_KEY)

@api_v1.route('/sql/analytics', methods=['POST'])
def analystic_sql():
    if request.method == 'POST':
        try:
            db_uri = request.json.get('db_uri')
            openai_api_key = request.json.get('openai_api_key')
            if openai_api_key:
                env_var(openai_api_key)
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
            env_var(OPENAI_KEY)


# 设置图片文件夹路径
IMAGE_FOLDER = 'images'
app.config['IMAGE_FOLDER'] = './temp'

@api_v1.route('/images/<path:filename>', methods=['GET'])
def image(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

from chatgpt import es_vector_search
@api_v1.route('/documents/qa', methods=['POST'])
def docments_qa():
    project_name = request.json.get('project_name')
    question = request.json.get('question')
    if not project_name:
        raise Exception('请输入项目名称')
    if not question:
        raise Exception('请输入问题')

    
    # try:
        # project_path = f'{os.getcwd()}/documents/{project_name}'
        # if not os.path.exists(project_path):
        #     raise Exception('项目不存在')
        # txt_docs = []
        # for root, dirs, files in os.walk(project_path):
        #         for file in files:
        #             file_type=file.split('.')[-1]
        #             if file_type == 'txt':
        #                 txt_docs.extend(TextLoader(os.path.join(root, file)).load())
        #             elif file_type=='docx':
        #                 txt_docs.extend(Docx2txtLoader(os.path.join(root, file)).load())
        #             elif file_type=='pdf':
        #                 txt_docs.extend(PyPDFLoader(os.path.join(root, file)).load())
    txt_docs = es_vector_search(question)
    print(txt_docs)
    answer = qa_with_doc(txt_docs, question)

    return {'code': 200, 'result': answer}
    # except Exception as e:
    #     return {'code': '100', 'message': f'{str(e)}'}

app.register_blueprint(api_v1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)