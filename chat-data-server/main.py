from flask import Flask, request
import os
from flask_cors import CORS
from chatgpt import file_agent

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/home/caidong/Program/ChatDataExpert/chat-data-server/upload_file'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {'message': '文件上传成功'}
        
@app.route('/analystic', methods=['POST'])
def analystic_file():
    print(request.form.get('prompt'))
    print(request.form.get('file_name'))

    if request.method == 'POST':
        agent=file_agent('./upload_file/allintitle%3A_Google Goes Gaga Parte 1 Legendado”_eea049eebff97e00a48f34e56c5ac31c.csv')
        result = agent.run('有多少行记录')
        print(result)
        return {'message': '文件上传成功'}

if __name__ == '__main__':
    app.run(debug=True)
