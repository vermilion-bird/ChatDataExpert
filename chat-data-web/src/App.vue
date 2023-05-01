<template>
<div class="container">
    <el-row :gutter="22" class="upload-file">
        <el-col :span="18" :offset="2" v-if="showTabel">
            <div class="wrapper">
                <el-divider content-position="left">【Data】FirstStep: File Upload Completed and Data Preview</el-divider>
                <el-button type="plain" icon="el-icon-refresh" @click="handleRefresh">Reload</el-button>
            </div>
            <el-table :data="tableData" max-height="50vh" border="true" show-overflow-tooltip="true" stripe="true" fit="true">
                <el-table-column v-for="column in tableColumns" :key="column.prop" :label="column.label" :prop="column.prop" min-width="100px">
                    <template v-slot:default="scope">
                        <div class="custom-cell">{{ scope.row[column.prop] }}</div>
                    </template>
                </el-table-column>
            </el-table>
        </el-col>

        <el-col :span="18" :offset="2" v-else>
            <el-divider content-position="left">【Data】FirstStep: Upload a data file in CSV or XLSX format</el-divider>
            <el-upload :on-success="handleSuccess" :on-error="handleError" class="" drag :action="upload_file_url">
                <el-icon class="el-icon--upload">
                    <upload-filled />
                </el-icon>
                <div class="el-upload__text">
                    Drop file here or <em>click to upload</em>
                </div>
                <template #tip>
                    <div class="el-upload__tip">
                        csv/xlsx files
                    </div>
                </template>
            </el-upload>
        </el-col>
    </el-row>
    <el-row :gutter="20" class="input-block">
        <el-col :span="18" :offset="2">
            <el-divider content-position="left">【Prompt】SecondStep: Write down the analysis requirements</el-divider>
            <div v-loading="loading">
                <el-input v-model="prompt" autosize placeholder="Please describe your data analysis needs.If you haven't uploaded a file, please upload it first." @keyup.enter="getAnalysic" :disabled="input_status">
                    <template #append>
                        <el-button @click="getAnalysic" :disabled="input_status">Execute</el-button>
                    </template>
                </el-input>
            </div>
        </el-col>
    </el-row>
    <el-row :gutter="20" class="result-block">
        <el-col :span="18" :offset="2">
            <el-divider content-position="left">【Result】ThirdStep: Present the data results.</el-divider>
            <div v-html="analysic_result" class="result" style="background-color: #ffffff" />
        </el-col>
    </el-row>
</div>
</template>

<script>
import {
    post,
    BASE_URL
} from './util/http';
import {
    UploadFilled
} from '@element-plus/icons-vue'
import {
    ElButton,
    ElIcon
} from 'element-plus';

export default {
    name: 'App',
    data() {
        return {
            input_status: true,
            loading: false,
            showTabel: false,
            upload_file_url: `${BASE_URL}/upload`,
            prompt: '',
            file_name: '',
            analysic_result: '',
            tableColumns: [],
            tableData: []
        }
    },
    components: {
        // HelloWorld
        UploadFilled,
        ElButton,
        ElIcon
    },
    computed: {},
    methods: {
        handleSuccess(response, file, fileList) {
            if (response.code != 200) {
                this.$message({
                    message: response.message,
                    type: 'error',
                    duration: 10 * 1000, // 600秒 * 1000毫秒/秒
                });
                fileList.pop()
                return
            }
            this.file_name = file.name
            this.showTabel = true
            console.log('文件上传成功', response, file, fileList);
            this.tableColumns = response.tableColumns
            this.tableData = response.tableData
            this.input_status = false
        },
        handleError(error, file, fileList) {
            this.$message({
                message: '文件上传失败' + file + error,
                type: 'error',
                duration: 600 * 1000, // 600秒 * 1000毫秒/秒
            });
            console.log('文件上传失败', error, file, fileList);
        },
        async getAnalysic() {
            try {
                this.loading = true
                var result = await post('/analystic', {
                    "file_name": this.file_name,
                    "prompt": this.prompt
                });
                if (result.code != 200) {
                    this.$message({
                        message: '数据分析失败，' + result.message,
                        type: 'error',
                        duration: 10 * 1000, // 600秒 * 1000毫秒/秒
                    });
                }
                this.analysic_result = result.thought

            } catch (error) {
                this.$message({
                    message: '数据分析失败，' + error.message,
                    type: 'error',
                    duration: 10 * 1000, // 600秒 * 1000毫秒/秒
                });
                console.error('请求失败', error);
            }
            this.loading = false
        },
        handleRefresh() {
            location.reload(); // 重新加载当前页面
        }
    },
}
</script>

<style>
.wrapper {
    display: flex;
    /* 设置为弹性盒子布局 */
    align-items: center;
    /* 垂直居中对齐 */
}

.el-divider {
    flex: 1;
    /* 分隔线自动占据剩余空间 */
}

.el-button {
    margin-left: 10px;
    /* 按钮和分隔线之间留出一定的间距 */
}

.custom-cell {
    max-height: 100px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.el-table th {
    white-space: nowrap !important;
    width: auto !important;
}

.multiline-text {
    white-space: pre-wrap;
}

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}

.result {
    white-space: pre-wrap;
    width: 100%;
    height: 100%;
    background-color: #859f98;
    align-items: center;
    flex-direction: column;
    text-align: left;
    box-sizing: border-box;
    padding: var(--el-empty-padding);
}

.search-btn {
    float: left;
    margin-right: 10px;
}

.input-block {
    margin-top: 20px;
}

.upload-file {
    margin-top: 20px;
}

.result-block {
    margin-top: 20px;
}
</style>
