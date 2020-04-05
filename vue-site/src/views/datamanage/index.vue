<template>
    <el-main>
        <el-form :inline="true">
            <el-form-item label="模板名称:">
                <el-input v-model="search" placeholder=""></el-input>
            </el-form-item>
        </el-form>



        <el-table :data="NewItems" style="width: 100%">
            <el-table-column label="数据名称" prop="dataName">
            </el-table-column>
            <el-table-column label="使用模板" prop="templateName">
            </el-table-column>
            <el-table-column label="创建时间" prop="createTime">
            </el-table-column>
            <el-table-column label="操作">
                <template slot-scope="scope">
                    <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="mini" @click="downloadData(scope.$index, scope.row)">下载数据</el-button>
                    <el-button size="mini" @click="downloadpdf(scope.$index, scope.row)">下载pdf</el-button>
                    <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
    </el-main>
</template>

<style>
    /*  .demo-table-expand {
    font-size: 0;
  }
  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }
  .demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  } */
</style>

<script>
    export default {
        data() {
            return {
                search: "",
                template: "",
                tableData: [],
                temp: []
            }
        },
        methods: {
            downloadData(row) {
                var _that = this
                console.log(row)
                this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/downloadData", this.tableData[row],
                    function(res) {
                        console.log(res.data)
                        let a = document.createElement('a');
                        let blob = new Blob([JSON.stringify(res.data, null, 4)], {
                            type: "application/json"
                        });
                        let objectUrl = URL.createObjectURL(blob);
                        a.setAttribute("href", objectUrl);
                        a.setAttribute("download", _that.tableData[row].name + '.json');
                        a.click();
                        document.body.removeChild(a); // 下载完成移除元素
                        window.URL.revokeObjectURL(objectUrl); // 释放掉blob对象

                    })
            },
            downloadpdf(row) {
                console.log(row)
                var _that = this
                console.log(row)
                this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/downloadPdf", this.tableData[row],
                    function(res) {
                        let a = document.createElement('a');
                        a.setAttribute("href", "data:application/octet-stream;base64," + res.data);
                        a.setAttribute("download", _that.tableData[row].name + '.pdf');
                        a.click();
                        document.body.removeChild(a); // 下载完成移除元素
                    })
            },
            handleEdit(row) {
                console.log(row)
                this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/editData", this.tableData[row],
                    function(res) {
                        console.log(res.data)
                    })

                this.$router.push({
                    name: 'pdfrender'
                })

            },
            handleDelete(row) {
                console.log(row)
                this.$axios.post(this.$client.apiUrlprefix() + "/reportmanage/delData", this.tableData[row],
                    function(res) {
                        console.log(res.data)
                    })
            }
        },
        mounted() {
            if (window.localStorage.getItem('currentTemplate') != null){
                this.search = window.localStorage.getItem('currentTemplate').replace(".json", "")
                window.localStorage.setItem('currentTemplate', "")
            }
            var _that = this
            this.$client.notifyws.notifyBus.$on("dataList", function(res) {
                console.log(res.data.dataList)
                _that.tableData = res.data.dataList
            })

            this.$axios.get(this.$client.apiUrlprefix() + "/reportmanage/dataList", {}, function(res) {
                console.log(res.data.message)
                if (res) {
                    if (res.data.retcode == 0) {
                        console.log(res.data.message)
                        _that.tableData = res.data.message
                        return true;
                    } else {
                        return false;
                    }
                }
            })
        },
        computed: {
            NewItems() {
                var _that = this;
                var NewItems = [];
                this.tableData.map(function(item) {
                    if (item.templateName.search("^" + _that.search) == 0) {
                        NewItems.push(item);
                    }
                });
                return NewItems;
            }
        }
    };
</script>
