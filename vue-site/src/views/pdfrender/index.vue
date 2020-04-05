<template>

    <el-row>
        <el-col :span="12">
            <el-button @click="pdfrender()" type="success" style="margin: 10px;">生成报告</el-button>
            <el-button @click="formatData()" type="primary" style="margin: 10px;">{{formatButtonValue}}</el-button>
            <el-button @click="dialogFormVisible = true" type="primary" style="margin: 10px;">保存</el-button>
            <el-dialog title="保存数据" :visible.sync="dialogFormVisible">
              <el-form>
                <el-form-item label="数据名称">
                  <el-input v-model="dataName" auto-complete="off"></el-input>
                </el-form-item>
                <el-form-item label="同时保存pdf">
                    <el-switch
                      v-model="createPdf"
                      active-color="#13ce66"
                      inactive-color="#ff4949">
                    </el-switch>
                </el-form-item>
              </el-form>
              <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="save()">确 定</el-button>
              </div>
            </el-dialog>
           <el-dialog title="请输入以下参数" :visible.sync="formatArgsVisible">
              <el-form>
                <el-form-item label="数据库类型" v-if="formatArgs.needDbtype">
                      <el-select placeholder="请选择" v-model="formatArgs.dbtype">
                        <el-option
                          v-for="item in formatArgs.dbtypeList"
                          :key="item"
                          :label="item"
                          :value="item">
                        </el-option>
                      </el-select>
                </el-form-item>
                <el-form-item label="用户数量" v-if="formatArgs.needCustomer">
                  <el-input v-model="formatArgs.customer" auto-complete="off" ></el-input>
                </el-form-item>
                <el-form-item label="导入数据时间" v-if="formatArgs.needDataLoad">
                  <el-input v-model="formatArgs.dataLoad" auto-complete="off" ></el-input>
                </el-form-item>
                <el-form-item label="同时保存pdf">
                    <el-switch
                      v-model="createPdf"
                      active-color="#13ce66"
                      inactive-color="#ff4949">
                    </el-switch>
                </el-form-item>
              </el-form>
              <div slot="footer" class="dialog-footer">
                <el-button @click="formatArgsVisible = false">取 消</el-button>
                <el-button type="primary" @click="formatWithArgs()">确 定</el-button>
              </div>
            </el-dialog>
            <div class="codemirror">
                <codemirror v-model="data" :options="cmOptions"></codemirror>
            </div>
        </el-col>
        <el-col :span="12">
            <div class="pdfpreview">
                <object :data=url type="application/pdf" width="50%" height="100%" internalinstanceid="41"></object>
            </div>
            
        </el-col>
    </el-row>


</template>

<script>
    // require component
    import {
        codemirror
    } from 'vue-codemirror'

    // require styles//
    import 'codemirror/lib/codemirror.css'
    import 'codemirror/mode/python/python.js'
    import 'codemirror/theme/mbo.css'
    import 'codemirror/theme/monokai.css'
    import 'codemirror/addon/selection/active-line.js'
    import 'codemirror/addon/edit/closebrackets.js'

    // component
    export default {
        components: {
            codemirror
        },
        data() {
            return {
                formatArgs:{
                    dbtype:"oracle",
                    customer:"5000",
                    dataLoad:"1800",
                    needDbtype:false,
                    needCustomer:false,
                    needDataLoad:false,
                    dbtypeList:['oracle', 'dm', 'mysql', 'kingbase', 'sqlserver']
                },
                formatArgsVisible:false,
                formatButtonValue:"格式化数据",
                isFormate:false,
                model: {},
                dataName: "",
                data: "",
                url: "",
                form:[],
                createPdf: true,
                dialogFormVisible: false,
                cmOptions: {
                    // codemirror options
                    styleActiveLine: true,
                    tabSize: 4,
                    indentUnit: 4, // 智能缩进单位为4个空格长度
                    indentWithTabs: true, // 使用制表符进行智能缩进
                    mode: 'text/x-python',
                    //keyMap: "sublime", // 快键键风格  会导致next错误
                    smartIndent: true, //智能缩进
                    lineWrapping: true, //
                    theme: 'monokai',
                    lineNumbers: true,
                    line: true,
                    gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
                    highlightSelectionMatches: {
                        showToken: /\w/,
                        annotateScrollbar: true
                    },
                    foldGutter: true,
                    closebrackets: true
                    // more codemirror options, 更多 codemirror 的高级配置...
                }
            }
        },
        methods: {
            formatWithArgs(){
                var _that = this
                if(this.isFormate === false){
                    console.log(this.model)
                    this.model.dataJson = JSON.parse(this.data)
                    this.model.dataJson.dbtype = this.formatArgs.dbtype
                    this.model.dataJson.customer = this.formatArgs.customer
                    this.model.dataJson.dataLoad = this.formatArgs.dataLoad
                    this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/formatData", this.model, function(
                        res) {
                        console.log(res.data)
                        _that.data = JSON.stringify(res.data.message, null, 4)
                    })
                    this.formatArgsVisible = false
                    this.isFormate = true
                    this.formatButtonValue = "取消格式化"
                }
            },
            formatData(){
                if(this.isFormate === false){
                    if (this.model.templateName.search('tpce') === 0){
                        this.formatArgsVisible = true
                        this.formatArgs.needCustomer = true
                        this.formatArgs.needDbtype = true
                    }
                    else if(this.model.templateName.search('tpcds') === 0){
                        this.formatArgsVisible = true
                        this.formatArgs.needCustomer = true
                        this.formatArgs.needDbtype = true
                        this.formatArgs.needDataLoad = true
                    }
                    else{
                        var _that = this

                            console.log(this.model)
                            this.model.dataJson = JSON.parse(this.data)
                            this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/formatData", this.model, function(
                                res) {
                                console.log(res.data)
                                _that.data = JSON.stringify(res.data.message, null, 4)
                            })
                            this.formatButtonValue = "取消格式化"
                            this.isFormate = true
                        }
                }
                else{
                    this.isFormate = false
                    this.formatButtonValue = "格式化数据"
                    this.data = JSON.stringify(this.model.dataJson, null, 4)
                }

            },
            onCmReady(cm) {
                console.log('the editor is readied!', cm)
            },
            onCmFocus(cm) {
                console.log('the editor is focus!', cm)
            },
            onCmCodeChange(newCode) {
                console.log('this is new code', newCode)
                this.data = newCode
            },
            pdfrender() {
                console.log('渲染脚本');
                var _that = this;
                this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/setData", JSON.parse(this.data), function(
                    res) {
                    console.log(res.data)
                })
                this.$axios.get(this.$client.apiUrlprefix() + "/reportmanage/pdfGenerate", {}, function(res) {
                    console.log(res.data.message)
                    _that.url = _that.$client.apiUrlprefix() + "/report/run?key=" + res.data.message;

                })
            },
            save() {
                if (this.model.dataModel.dataPath == undefined){
                    // 创建新的data的 json文件
                    this.model.dataModel.dataPath = this.model.dataModel.dirPath + this.dataName + '.json'
                    this.model.createPdf = this.createPdf 

                    this.model.dataModel.dataName = this.dataName
                    this.model.dataJson = JSON.parse(this.data)
                }
                else{
                    // 保存覆盖已有的data json文件
                    this.model.createPdf = this.createPdf
                    this.model.dataModel.dataPath = this.model.dataModel.dataPath.replace(this.model.dataModel.dataName, this.dataName)
                    this.model.dataModel.dataName = this.dataName
                    this.model.dataJson = JSON.parse(this.data)
                }
                this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/saveData", this.model, function(
                    res) {
                    console.log(res.data)
                })
                this.dialogFormVisible = false
            }
        },
        mounted() {
            var _that = this
            this.$axios.get(this.$client.apiUrlprefix() + "/reportmanage/getData", {}, function(res) {
                console.log(res.data.message)
                if (res) {
                    if (res.data.retcode == 0) {
                        // 将json 转换为 string 并且 优美展示
                        console.log(res.data.message)
                        _that.model = res.data.message
                        _that.data = JSON.stringify(res.data.message.dataJson, null, 4);
                        _that.dataName = res.data.message.dataModel.dataName
                        return true;
                    } else {
                        return false;
                    }
                }
            })

        }

    }
</script>
<style>
    .CodeMirror {
        overflow-y: scroll;
        height: 900px;
    }

    .CodeMirror-focused .cm-matchhighlight {
        background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAFklEQVQI12NgYGBgkKzc8x9CMDAwAAAmhwSbidEoSQAAAABJRU5ErkJggg==);
        background-position: bottom;
        background-repeat: repeat-x;
    }

    .cm-matchhighlight {
        background-color: lightgreen
    }

    .CodeMirror-selection-highlight-scrollbar {
        background-color: green
    }

    .pdfpreview {
        height: calc(100% - 50px);
        width: 100%;
        position: absolute;
        top: 45px;
    }
</style>
