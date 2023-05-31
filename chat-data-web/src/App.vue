<template>
<div>
    <el-tabs v-model="activeTab" type="border-card" tab-position="top">
        <el-tab-pane label="ChatPandas" name="tab1">
            <chat-dataframe></chat-dataframe>
        </el-tab-pane>
        <el-tab-pane label="ChatSQL" name="tab2">
            <chat-sql></chat-sql>
        </el-tab-pane>
        <el-tab-pane label="ChatMatplot" name="tab3">
            <chat-matplotlib></chat-matplotlib>
        </el-tab-pane>
        <el-tab-pane label="ChatDoc" name="tab4">
            <chat-doc></chat-doc>
        </el-tab-pane>
    </el-tabs>
</div>
</template>

<script>
import ChatDataframe from './components/ChatDataframe.vue'
import ChatSql from './components/ChatSql.vue'
// import ConfigPage from './components/ConfigPage.vue'
import ChatMatplotlib from './components/ChatMatplotlib.vue'
import ChatDoc from './components/ChatDoc.vue'

export default {
    name: "App",
    components: {
        ChatDataframe,
        ChatSql,
        ChatMatplotlib,
        ChatDoc,
        // ConfigPage
    },
    data() {
        return {
            activeTab: 'tab1',
            keyContainer: true
        }
    },
}
</script>

<style scoped>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 20px;
}
</style>
