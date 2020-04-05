import Vue from "vue"

var notifyws = new WebSocket("ws://" + document.domain + ":8800/ws/api/v1/notify");

window.notifyws = notifyws;

notifyws.notifyBus = new Vue();

notifyws.onopen = function(event)
{
  console.log("notifyws websocket is conneted!", event);
};

notifyws.onmessage = function (event) {
  var message = JSON.parse(event.data);
  console.log(message);
  console.log(message["type"]);
  notifyws.notifyBus.$emit(message["type"], message);
};

notifyws.onerror = function (event) {
    console.log(event);
};


notifyws.onclose = function(event)
{ 
  // 关闭 websocket
  console.log("notifyws websocket is colosed!", event);
  notifyws = new WebSocket("ws://" + document.domain + ":8800/ws/api/v1/notify");
};

export default notifyws;
