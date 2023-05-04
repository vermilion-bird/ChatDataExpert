<template>
<div style="margin-bottom:10px">
    <p>开发者api key 使用量超限, 请申请OpenAI KEY 
        <br/>
        <el-link href="https://www.notion.so/caidong/OpenAI-Key-711f2484037f4fcfa01b5cbb2cda5b91?pvs=4" type="warning">申请教程</el-link>
        <span>&nbsp; &nbsp;</span>
        <el-link href="https://platform.openai.com/account/usage" type="info">申请地址</el-link>
    </p>
    <div class="key_container">
        <div class="label">OpenAI Key: </div>
        <div class="input">
            <el-input @change="key_change" v-model="openai_api_key" placeholder="Please input sk-****" clearable />
        </div>
    </div>
    <el-alert style="margin-top:10px" title="提示: 使用后,请及时在OpenAI 后台删除Key" type="error" />
</div>
</template>

<script>
export default {
    name: "ConfigPage",
    components: {},
    data() {
        return {
            openai_api_key: '',
        }
    },
    created() {
        const openai_api_key = localStorage.getItem("openai_api_key");
        if (openai_api_key) {
            this.openai_api_key = openai_api_key;
        }
    },
    methods: {
        key_change(val) {
            localStorage.setItem("openai_api_key", val);
            // const message = localStorage.getItem("openai_api_key");
            // console.log(message)
        }
    },
}
</script>

<style>
.key_container {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
}

.label {
    flex: 0 0 auto;
    /* 固定宽度 */
    width: 120px;
    /* 固定宽度 */
    margin-right: 20px;
    /* 标签和输入框之间的间距 */
}

.input {
    flex: 1 1 auto;
    /* 自适应宽度 */
}
</style>
