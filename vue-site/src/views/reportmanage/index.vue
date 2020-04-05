<template>
    <div>
        <div>
            <el-form :inline="true" ref="ruleForm" label-width="100px" class="demo-ruleForm" style="padding: 10px; padding-bottom: 0px;">
                <el-form-item>
                    <el-button type="primary" @click="dialogFormVisible = true">新建模板</el-button>
                </el-form-item>
            </el-form>
            <el-dialog title="新建模板" :visible.sync="dialogFormVisible" style="height: auto;">
                <el-form>
                    <el-form-item label="模板名称">
                        <el-input v-model="templateName" auto-complete="off"></el-input>
                    </el-form-item>
                    <el-form-item label="继承已有模板">
                        <el-switch v-model="useTemplate" active-color="#13ce66" inactive-color="#ff4949">
                        </el-switch>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="primary" @click="newTemplate()">确 定</el-button>
                </div>
                <div v-if="useTemplate">
                    <el-select v-model="selectValue" filterable placeholder="请选择">
                        <el-option v-for="item in tableData" :key="item" :label="item" :value="item">
                        </el-option>
                    </el-select>
                </div>
            </el-dialog>

            <el-table :data=tableData.slice((currentPage-1)*pageSize,currentPage*pageSize) style="width: 100%">
                <el-divider></el-divider>
                <el-table-column label="报告名称" width="400">
                    <template slot-scope="props">
                        <span style="margin-left: 10px">{{ props.row }}</span>
                    </template>
                </el-table-column>
                <el-table-column label="操作">
                    <template slot-scope="scope">
                        <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                        <el-button size="mini" @click="handleRender(scope.$index, scope.row)">报告生成</el-button>
                        <el-button size="mini" @click="dataManage(scope.$index, scope.row)">数据管理</el-button>
                        <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <div>
            <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
                :page-sizes="[10, 20, 30, 50, 100]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper"
                :total="tableData.length" width="300">
            </el-pagination>
        </div>
    </div>
</template>



<script>
    export default {
        data() {
            return {
                selectValue: "",
                dialogFormVisible: false,
                useTemplate: true,
                tableData: [],
                templateName: "",
                action: this.$client.apiUrlprefix() + "/reportmanage/upload/template",
                fileList: [],
                isPagination: false,
                // 当前页
                currentPage: 1,
                // 每页多少条
                pageSize: 10,
            }
        },
        methods: {
            newTemplate() {
                console.log("newTemplate")
                this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/newTemplate", {
                    "templateName": this.templateName,
                    "sample": this.selectValue
                }, function(res) {
                    console.log(res.data.message)
                })
                this.dialogFormVisible = false
            },
            handleSizeChange(val) {
                this.pageSize = val;
            },
            // 当前页
            handleCurrentChange(val) {
                this.currentPage = val;
            },
            handleEdit(index, row) {
                console.log(index, row);
                this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/setTemplate", {
                    "name": row
                }, function(res) {
                    // let template = res.data.message.template
                    // console.log(template)
                    // localStorage.setItem("template", JSON.stringify(template));

                    if (res) {
                        if (res.data.retcode == 0) {
                            return true;
                        } else {
                            return false;
                        }
                    }
                })
                this.$router.push({
                    name: 'reportedit'
                })
            },
            dataManage(index, row) {
                window.localStorage.setItem('currentTemplate', row)
                this.$router.push({
                    name: 'datamanage'
                })
            },
            handleDelete(index, row) {
                console.log(index, row);
                this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/delTemplate", {
                    "templateName": row
                }, function(res) {
                    console.log(res)
                    if (res) {
                        if (res.data.retcode == 0) {
                            return true;
                        } else {
                            return false;
                        }
                    }
                })
            },
            handleRender(index, row) {
                console.log(index, row);
                this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/setTemplate", {
                    "templateName": row
                }, function(res) {
                    // let template = res.data.message.template
                    // console.log(template)
                    // localStorage.setItem("template", JSON.stringify(template));
                    if (res) {
                        if (res.data.retcode == 0) {
                            return true;
                        } else {
                            return false;
                        }
                    }
                })
                this.$router.push({
                    name: 'pdfrender'
                })
            }
        },
        mounted() {
            var _that = this;
            this.$client.notifyws.notifyBus.$on("templatesList", function(res) {
                    console.log(res.data.templatesList)
                    _that.tableData = res.data.templatesList
                }),

                this.$axios.get(this.$client.apiUrlprefix() + "/reportmanage/templatesList", {}, function(res) {
                    console.log(res)
                    if (res) {
                        if (res.data.retcode == 0) {
                            console.log(res.data.message.templatesList)
                            _that.tableData = res.data.message.templatesList

                            return true;
                        } else {
                            return false;
                        }
                    }
                })
        }
    }
</script>
