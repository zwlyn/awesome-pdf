<template>

    <!--        <iframe id="show-iframe" frameborder="0" scrolling="yes" style="background-color:transparent; position：absolute;width: 100%;
     height:1000px; top: 0;left:0;bottom:0;"
         src='http://localhost:8800/report'></iframe> -->
    <div id="reportbro"></div>

</template>

<script>
    export default {
        data() {
            return {}
        },
        methods: {

        },
        created() {

        },
        
    mounted() {
        var $ =  window.$
        var _that = this
        var rb;
        
        function saveReport() {
            var report = rb.getReport();
            $.ajax({
                url: _that.$client.apiUrlprefix() + "/report/save",
                data: JSON.stringify(report),
                type: "post",
                contentType: "application/json",
                dataType: 'json',
                success: function (data) {
                    console.log(data);
                    if (data.retcode == 0) {
                        alert('save successful');
                    } else {
                        alert(data.message);
                    }
                }
            });
        }
        
        rb = $("#reportbro").reportBro({
            reportServerUrl: _that.$client.apiUrlprefix() + "/report/run",
            saveCallback: saveReport,
            showGrid: true,
            adminMode: true,
            enableSpreadsheet: false
        });
        
        $.ajax({
            url: _that.$client.apiUrlprefix() + "/load",
            type: "GET",
            contentType: "application/json",
            dataType: 'json',
            success: function (data) {
                $('#reportbro').reportBro('load', data);
            }
        });
        
    }

    }
</script>
