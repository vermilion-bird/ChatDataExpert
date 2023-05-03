<template>
<el-row :gutter="20" class="input-block">
    <el-col :span="18" :offset="2">
        <p>A simulated order table in the database.</p>
        <img :src="imgUrl" class="responsive"/>
        <p style="margin-top: 20px">If you want to connect to your own database, please ensure that the database is available and can be accessed remotely, Please enter the database connection address.</p>
        <p>You can use the test database provided above; please leave the following input box empty.        </p>
        <el-input  v-model="db_uri" placeholder="example  mysql+mysqlconnector://user:password@172.17.0.4:3306/database" />
        <el-divider content-position="left">【Prompt】FirstStep: Write down the analysis requirements</el-divider>
        <div v-loading="loading">
            <el-input v-model="prompt" autosize placeholder="Please describe your data analysis needs." @keyup.enter="getSQLAnalysic" :disabled="input_status">
                <template #append>
                    <el-button @click="getSQLAnalysic" :disabled="input_status">Execute</el-button>
                </template>
            </el-input>
        </div>
    </el-col>
</el-row>
<el-row :gutter="20" class="result-block">
    <el-col :span="18" :offset="2">
        <el-divider content-position="left">【Result】SecondStep: Present the data results.</el-divider>
        <div v-html="analysic_result" class="result" style="background-color: #ffffff" />
    </el-col>
</el-row>
</template>

<script>
import {
    post
} from '../util/http';
import imgUrl from '@/assets/order.png';

export default {
    name: "ChatSql",
    components: {},
    data() {
        return {
            loading: false,
            prompt: '',
            db_uri: '',
            analysic_result: '',
            imgUrl:imgUrl,
        }
    },
    methods: {
        async getSQLAnalysic() {
            try {
                this.loading = true
                var result = await post('/sql/analytics', {
                    "db_uri": this.db_uri,
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
        }
    }
}
</script>
<style scoped>
  /* 使图片具有响应式布局 */
  img.responsive {
    max-width: 100%; /* 限制图片的最大宽度为其父容器的宽度 */
    height: auto;    /* 保持图片的纵横比 */
    display: block;  /* 让图片成为块级元素以消除下方的空白间距 */
}
</style>