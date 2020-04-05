import Vue from "vue"
import notifyws from "./notifywsapi.js"
import dateFormat from "dateformat"

var client = {
    rootUrl: window.location.protocol + "//" + window.location.hostname + ":8800",
    apiUrlprefix: function(){
    return this.rootUrl + "/report"
    },
    eventBus: new Vue(),
    notifyws: notifyws,

    value2CheckedList(value, options, length){
        if (value === undefined){
          return;
        }
        var bits = value.toString(2);
        var bitsCount = bits.length;
        for (var i = 0; i < length - bitsCount; i++) {
            bits = "0" + bits;
        }
        bits = bits.split("").reverse().join("");
        var ret = [];
        for (i = 0; i < bits.length; i++) {
            if (bits[i] === "1"){
                ret.push(options[i])
            }
        }
        return ret;
    },

    checkedList2Value(checkedList, options, length){
        var bits = "";
        for (var i = 0; i < length; i++) {
            if (checkedList.indexOf(options[i]) != -1){
                bits += "1";
            }else{
                bits += "0";
            }
        }

        bits = bits.split("").reverse().join("");
        return parseInt(bits, 2);
    },

    notify: function(that, event, res){
        if (res === undefined){
          return false;
        }
        if (res.data.code == 0){
          that.$notify({
            title: event.srcElement.innerText + that.title + '成功',
            message: res.data.message,
            type: 'success',
            duration: 2000,
          });
          return true;
        }else {
          that.$notify({
            title: event.srcElement.innerText + that.title + '失败',
            message: res.data.message,
            type: 'error',
            duration: 5000
          });
          return false;
        }
      },

      notifyInfo: function (that, title, message, duration, dangerouslyUseHTMLString) {
        that.$notify({
            title: title,
            message: message,
            type: 'info',
            duration: duration,
            dangerouslyUseHTMLString: dangerouslyUseHTMLString
          });
      },

      notifySuccess: function (that, title, message, duration, dangerouslyUseHTMLString) {
        that.$notify({
            title: title,
            message: message,
            type: 'success',
            duration: duration,
            dangerouslyUseHTMLString: dangerouslyUseHTMLString
          });
      },

      notifyError: function (that, title, message, duration, dangerouslyUseHTMLString) {
        that.$notify({
            title: title,
            message: message,
            type: 'error',
            duration: duration,
            dangerouslyUseHTMLString: dangerouslyUseHTMLString
          });
      },

      // timeStamp: MSecsSinceEpoch = Unix timestamp * 1000
      parseTimeStamp(timeStamp) {
        return dateFormat(
          this.ts2Date(timeStamp),
          "yyyy-mm-dd HH:MM:ss"
        );
      },
      ts2Date(strTimestamp) {
        var timestamp = parseInt(strTimestamp);
        if (isNaN(timestamp)) {
          timestamp = 0;
        }
        return new Date(timestamp);
      }
}

export function deepCopy(obj) {
  var str, newobj = obj.constructor === Array ? [] : {};
    if(typeof obj !== 'object'){
        return;
    } else if(window.JSON){
        str = JSON.stringify(obj), //系列化对象
        newobj = JSON.parse(str); //还原
    } else {
        for(var i in obj){
            newobj[i] = typeof obj[i] === 'object' ?
            deepCopy(obj[i]) : obj[i];
        }
    }
    return newobj
}

export function setCache(key, value) {
    localStorage.setItem(key, JSON.stringify(value))
}

export function getCache(key) {
    return JSON.parse(localStorage.getItem(key))
}


export default client;