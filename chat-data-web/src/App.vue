<template>
<div class="container">
    <el-row :gutter="20" class="upload-file">
        <el-col :span="12" :offset="6">
            <el-upload :on-success="handleSuccess" :on-error="handleError" class="" drag action="http://localhost:5000/upload" multiple>
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
        <el-col :span="12" :offset="6">
            <el-input v-model="prompt" autosize placeholder="请描述您的统计需求">
                <template #append>
                    <el-button @click="getAnalysic">提交</el-button>
                    <!-- <el-icon style="vertical-align: middle">
                        <Search />
                    </el-icon>
                    <span style="vertical-align: middle"> Search111 </span> -->

                </template>
            </el-input>
        </el-col>
    </el-row>
    <el-row :gutter="20" class="result-block">
        <el-col :span="12" :offset="6">
            <div class="result" style="background-color: #ffffff">{{analysic_result}}</div>
        </el-col>
    </el-row>
</div>
</template>

<script>
import {
    post
} from './util/http';

// import HelloWorld from './components/HelloWorld.vue'
import {
    UploadFilled
} from '@element-plus/icons-vue'

export default {
    name: 'App',
    data() {
        return {
            prompt: '',
            file_name: '',
            analysic_result: '',
        }
    },
    components: {
        // HelloWorld
        UploadFilled
    },
    methods: {
        handleSuccess(response, file, fileList) {
            this.file_name = file.name
            console.log(this.file_name)
            console.log('文件上传成功', response, file, fileList);
        },
        handleError(error, file, fileList) {
            console.log('文件上传失败', error, file, fileList);
        },
        async getAnalysic() {
            try {
                this.analysic_result = await post('/analystic', {
                    "file_name": this.file_name,
                    "prompt": this.prompt
                });
            } catch (error) {
                console.error('请求失败', error);
            }
        }
    },
}
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
}

.result {
    width: 100%;
    height: 100%;
    background-color: #ffffff;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    text-align: center;
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
