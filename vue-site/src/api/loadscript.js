export default function loadJs(url,_callback_success,_callback_fail){
    var callback_success = function (response) {
        console.log("load js success...",response);
    }
    var callback_fail = function (response) {
        console.log("load js fail...",response);
    }
    _callback_success = _callback_success || callback_success;
    _callback_fail = _callback_fail || callback_fail; 
    $.getScript(url).done(_callback_success).fail(_callback_fail);
}