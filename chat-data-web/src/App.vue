<template>
    <div>
        <el-tabs v-model="activeTab" type="border-card" tab-position="top">
            <el-tab-pane label="ChatPandas" name="tab1">
                <chat-dataframe></chat-dataframe>
            </el-tab-pane>
            <el-tab-pane label="ChatSQL" name="tab2">
                <chat-sql></chat-sql>
            </el-tab-pane>
            <!-- <el-tab-pane label="Conf" name="tab3">
                <chat-sql></chat-sql>
            </el-tab-pane> -->
        </el-tabs>
    </div>
</template>

<script>
import ChatDataframe from './components/ChatDataframe.vue'
import ChatSql from './components/ChatSql.vue'


export default {
    name: "App",
    components: {
        ChatDataframe,
        ChatSql,
    },
    data() {
        return {
            activeTab: 'tab1',
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