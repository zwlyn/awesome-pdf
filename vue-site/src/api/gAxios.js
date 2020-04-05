import axios from 'axios';

function encodeURI(params){
  let newData = '';
    for (let k in params) {
      if (params.hasOwnProperty(k) === true) {
        newData += encodeURIComponent(k) + '=' + encodeURIComponent(params[k]) + '&';
      }
    }
  return newData;
}

let http = axios.create({
  baseURL: 'http://localhost:8800/',
  withCredentials: false,
  headers: {
    "Content-Type": "application/json;charset=utf-8"
  }
});
    // 'Access-Control-Allow-Origin': '*',
    // "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
function apiAxios(method, url, params, response) {
  http({
    method: method,
    url: method === 'GET' && params != "" ? url + "?" + encodeURI(params) : url,
    data: method != 'GET' ? JSON.stringify(params) : null
  }).then(function (res) {
    if (res != undefined){
      response(res);
    }
  }).catch(function (err) {
    response(err.response);
  })
}

export default {
  get: function (url, params, response) {
    return apiAxios('GET', url, params, response)
  },
  post: function (url, params, response) {
    return apiAxios('POST', url, params, response)
  },
  put: function (url, params, response) {
    return apiAxios('PUT', url, params, response)
  },
  delete: function (url, params, response) {
    return apiAxios('DELETE', url, params, response)
  },
  jsonp: function (url, params, response) {
    return apiAxios('JSONP', url, params, response)
  },
}