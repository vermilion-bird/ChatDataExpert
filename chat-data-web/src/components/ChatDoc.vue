<template>
<div>
    <el-dialog title="请输入项目名" v-model="dialogVisible" width="300px" @close="closeDialog">
        <el-form>
            <el-form-item label="项目名">
                <el-input v-model="projectName" placeholder="请输入项目名"></el-input>
            </el-form-item>
        </el-form>
        <template v-slot:footer>
            <el-button @click="closeDialog">取消</el-button>
            <el-button type="primary" @click="confirmDialog">确定</el-button>
        </template>
    </el-dialog>
    <el-collapse v-model="activeNames">
        <el-collapse-item title="文档上传" :value="true" name="upload">
            <el-upload :on-success="handleSuccess" :on-error="handleError" class="" drag :http-request="uploadFile">
                <el-icon class="el-icon--upload">
                    <upload-filled />
                </el-icon>
                <div class="el-upload__text">
                    Drop file here or <em>click to upload</em>
                </div>
                <template #tip>
                    <div class="el-upload__tip">
                        PDF/DOCX/TXT files less than 100M
                    </div>
                </template>
            </el-upload>
        </el-collapse-item>
        <el-collapse-item title="文档列表" name="fileList">
            <el-table :data="docData" max-height="50vh" border>
                <el-table-column type="index"></el-table-column>
                <el-table-column prop="file_name" label="文件名"></el-table-column>
                <el-table-column prop="file_type" label="文件类型"></el-table-column>
                <el-table-column prop="file_size" label="文件大小(MB)"></el-table-column>
                <el-table-column prop="creation_time" label="文件创建时间"></el-table-column>
            </el-table>
        </el-collapse-item>
    </el-collapse>
    <div class="chat-container">
        <div v-for="(message, index) in messages" :key="index" :class="{ 'chat-message-right': message.user === 'You', 'chat-message-left': message.user !== 'You' }">
            <div class="chat-message-content">
                <p><strong>{{ message.user }}:</strong> {{ message.text }}</p>
            </div>
        </div>
        <div class="input-container" v-loading="loading">
            <el-input type="textarea" v-model="question" placeholder="对话聊天框" @keyup.enter="qa_doc"></el-input>
            <el-button style="margin-top:10px" type="primary" @click="qa_doc">问答</el-button>
        </div>
    </div>
</div>
</template>

<script>
import {
    ElCollapse,
    ElCollapseItem
} from 'element-plus';
import {
    UploadFilled
} from '@element-plus/icons-vue'
import {
    get,
    BASE_URL,
    post
} from '../util/http';
export default {
    name: 'ChatDoc',
    components: {
        ElCollapse,
        ElCollapseItem,
        UploadFilled
    },
    data() {
        return {
            loading: false,
            question: '',
            messages: [{
                user: 'AI',
                text: 'Hello! 我是问答机器人，欢迎提问，根据您的文档内容，努力给您满意答复'
            }],
            upload_file_url: `${BASE_URL}/upload`,
            dialogVisible: true,
            projectName: '',
            docData: [],
            fileList: [],
            newMessage: '',
            activeNames: ['upload', 'fileList']
        }
    },
    created() {
        this.projectName = localStorage.getItem('project_name')
        console.log(this.projectName)
        if (this.projectName != null) {
            this.dialogVisible = false
            this.list_dir()
        }
    },
    methods: {
        qa_doc() {
            this.loading = true
            this.messages.push({
                user: 'YOU',
                text: this.question
            })
            post('/documents/qa', {
                "project_name": this.projectName,
                "question": this.question
            }).then((res) => {
                if (res.code !== 200) {
                    this.$message({
                        message: res.message,
                        type: 'error',
                        duration: 10 * 1000, // 600秒 * 1000毫秒/秒
                    });
                    this.loading = false
                    return
                }
                this.messages.push({
                        user: 'AI',
                        text: res.result
                    }),
                    this.question = ''
                this.loading = false
            })
        },
        list_dir() {
            if (this.projectName === '') {
                return
            }
            get(`/list/dir?project_name=${this.projectName}`).then((res) => {
                if (res.code !== 200) {
                    this.$message({
                        message: res.message,
                        type: 'error',
                        duration: 10 * 1000, // 600秒 * 1000毫秒/秒
                    });
                    return
                }
                this.docData = res.files
            })
        },
        uploadFile(file) {
            let formData = new FormData();
            formData.append('file', file.file);
            formData.append('project_name', this.projectName);
            formData.append('file_type', 'document')
            post(this.upload_file_url, formData).then((res) => {
                if (res.code !== 200) {
                    this.$message({
                        message: res.message,
                        type: 'error',
                        duration: 10 * 1000, // 600秒 * 1000毫秒/秒
                    });
                    return
                }
                this.$message({
                    message: '上传成功',
                    type: 'success',
                    duration: 10 * 1000, // 600秒 * 1000毫秒/秒
                });
                this.list_dir()
            })

        },
        // handleError(err, file, fileList) {},
        // handleSuccess(res, file, fileList) {},
        closeDialog() {
            this.dialogVisible = false
        },
        confirmDialog() {
            get(`/create/project?project_name=${this.projectName}`).then((res) => {
                if (res.code !== 200) {
                    this.$message({
                        message: res.message,
                        type: 'error',
                        duration: 10 * 1000, // 600秒 * 1000毫秒/秒
                    });
                    return
                }
                this.$message({
                    message: '创建成功',
                    type: 'success',
                    duration: 10 * 1000, // 600秒 * 1000毫秒/秒
                });
                localStorage.setItem('project_name', this.projectName)
                this.dialogVisible = false
            })
        },
    }
}
</script>

<style>
.upload-demo {
    display: inline-block;
    margin-bottom: 10px;
    margin-left: 20px;
}

.chat-container {
    max-height: 1000px;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
    background-color: #f0f0f0;
}

.chat-message-left {
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 10px;
    background-color: #ffffff;
}
</style>
