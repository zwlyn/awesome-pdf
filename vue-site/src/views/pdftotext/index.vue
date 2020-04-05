<template>

    <el-row class="el-row">
        <el-col :span="8">
            <el-form :inline="true" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                <el-form-item>
                    <el-button style="margin-left: 10px;" size="small" type="success" @click="pdftotext">pdf转文本</el-button>
                    <el-button style="margin-left: 10px;" size="small" type="primary" @click="downloadText">下载文本</el-button>
                    <el-button style="margin-left: 10px;" size="small" type="primary" @click="clearPdfList">清空数据</el-button>
                </el-form-item>
            </el-form>
            <el-upload class="upload-demo" drag :action="action" :multiple="multiple" :on-preview="handlePreview"
                :on-remove="handleRemove" :before-remove="beforeRemove" :on-progress="handleProgress" :on-success="handleSucess"
                :file-list="fileList" name=pdf :limit="10" style="height: 1000px; margin: 10px;">
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                <div class="el-upload__tip" slot="tip">只能上传pdf文件</div>
            </el-upload>
        </el-col>
        <el-col :span="12">
            <div class="pdfpreview">
                <object :data=url type="application/pdf" width="65%" height="100%" internalinstanceid="41"></object>
            </div>
        </el-col>
    </el-row>

</template>
<script>
    export default {
        data() {
            return {
                activeNames: 0,
                action: this.$client.apiUrlprefix() + '/reportmanage/upload/pdf',
                multiple: false,
                fileList: [],
                glider_id: this.$route.params["id"],
                writeProgress: 0,
                readProgress: 0,
                fileType: "state",
                profile_id: 1,
                filename: "",
                url: null
            };
        },
        computed: {
        },
        methods: {
            pdftotext() {
                var _that = this
                console.log(this.fileList[0])
                let uploadPath = "uploadfiles\\" + this.fileList[0].name
                this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/pdftotext", {
                    uploadPath: uploadPath
                }, function(res) {
                    console.log(res.data)
                     _that.$client.notifySuccess(_that, "转换成功，可以下载了(*^_^*)");
                })
                //this.fileList = []
            },
            downloadText() {
                let textPath = "uploadfiles\\" + this.fileList[0].name.replace("pdf", "txt")
                this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/downloadText", {
                    textPath: textPath
                }, function(res) {

                    //let formData = new FormData();
                    //let res = await post(url, formData);
                    const conent = res.data
                    // console.log(conent);
                    console.log(res)
                    const blob = new Blob([conent])
                    console.log(blob)
                    const fileName = "翻译结果.txt"//res.data.name.replace("pdf", "txt")
                    const link = document.createElement('a')
                    link.download = fileName // a标签添加属性
                    link.style.display = 'none'
                    link.href = URL.createObjectURL(blob)
                    document.body.appendChild(link)
                    link.click() // 执行下载
                    URL.revokeObjectURL(link.href) // 释放url
                    document.body.removeChild(link) // 释
                })
            },
            clearPdfList() {
                var _that = this
                this.$axios.get(this.$client.apiUrlprefix() + "/reportmanage/clearPdfList", {}, function(res) {
                    console.log(res.data.message)
                    _that.fileList = []
                })
            },
            handleRemove(file, fileList) {
                console.log(file, fileList)
            },
            handlePreview(file) {
                console.log(file);
            },
            beforeRemove(file, fileList) {
                console.log(file, fileList)
                return this.$confirm(`确定移除 ${ file.name }？`);
            },
            handleProgress(event, file, fileList) {
                console.log(event, file, fileList);
                this.writeProgress = parseFloat(event.percent.toFixed(2));
            },
            handleSucess(response, file, fileList) {
                this.fileList = fileList;
                console.log(event, file, fileList)
            }
        },
        mounted() {
            // var _that = this;
            // this.$client.notifyws.notifyBus.$on("pdfList", function(res) {
            //         console.log(res.data)
            //         console.log(res.data)
            //         _that.fileList = res.data
            //     })
        }
    }
</script>
<style>
    /*    .el-upload {
        height: 1000px;
    } */

    .el-container {
        /*设置内部填充为0，几个布局元素之间没有间距*/
        padding: 0px;
        /*外部间距也是如此设置*/
        margin: 0px;
        /*统一设置高度为100%*/
        height: 100%;
        width: 100%;
    }

    #app {
        /*设置内部填充为0，几个布局元素之间没有间距*/
        padding: 0px;
        /*外部间距也是如此设置*/
        margin: 0px;
        /*统一设置高度为100%*/
        height: 100%;
        width: 100%;
    }

    .pdfpreview {
        height: calc(100% - 50px);
        width: 100%;
        position: absolute;
        top: 45px;
        z-index: 999;
    }
</style>
