/* global prefixURL */
import $ from 'jquery';
import { requests, contents } from '../config';
import { showAlert } from '../utils/alert';
import { removePath } from '../utils/history';


function loadModule() {
  let inProgress = [];

  function setLoader(wrapperEl, loading) {
    const loaderEl = wrapperEl.getElementsByClassName('loader')[0];
    loaderEl.dataset.loading = loading;
  }

  function get(id, request, param, callbackFunction = null) {
    const pathParam = !param ? id : param;
    const path = request.path;
    const url = `${prefixURL}/${path}${pathParam}/`;

    $.ajax({
      url,
      beforeSend(xhr) {
        request.xhr = xhr; // eslint-disable-line no-param-reassign
        inProgress.push(request.name);
        setLoader(request.wrapperEl, true);
      },
      success(xhr) {
        request.wrapperEl.insertAdjacentHTML('beforeend', xhr.html);
        if (request.name !== 'comments') {
          request.loadedIds.push(id);
        }
      },
      error(xhr) {
        if (xhr.status === 404) {
          const content = contents[request.content];
          content.wrapperEl.dataset[`${content.name}Open`] = 'false';
          removePath(content.name);
          showAlert(xhr.responseJSON.title, xhr.responseJSON.message, 'error', false);
        } else if (xhr.status !== 0 && xhr.statusText !== 'abort') {
          showAlert(xhr.responseJSON.title, xhr.responseJSON.message, 'error');
        }
      },
      complete() {
        const requestIndex = inProgress.indexOf(request.name);
        if (requestIndex > -1) inProgress.splice(requestIndex, 1);
        request.xhr = {}; // eslint-disable-line no-param-reassign
        setLoader(request.wrapperEl, false);
        if (callbackFunction) callbackFunction();
      },
    });
  }

  function getCSRF() {
    const value = `; ${document.cookie}`;
    const parts = value.split('; csrftoken=');
    if (parts.length === 2) {
      return parts.pop().split(';').shift();
    }
    return null;
  }

  function sendRequest(method, request, data, htmlInsertion = 'insert') {
    const path = request.path;
    let url = `${prefixURL}/${path}/`;
    if (path[0] === '/') url = path;
    if (path[path.length - 1] === '/') url = url.slice(0, url.length - 1);

    $.ajax({
      url,
      type: method,
      data,
      beforeSend(xhr) {
        if (!this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', getCSRF());
        }
        request.xhr = xhr; // eslint-disable-line no-param-reassign
      },
      success(xhr) {
        if (htmlInsertion === 'insert') {
          request.wrapperEl.insertAdjacentHTML('beforeend', xhr.html);
        } else if (htmlInsertion === 'replace') {
          request.wrapperEl.innerHTML = xhr.html; // eslint-disable-line no-param-reassign
        }
      },
      error(xhr) {
        showAlert(xhr.responseJSON.title, xhr.responseJSON.message, 'error');
      },
      complete() {
        request.xhr = {}; // eslint-disable-line no-param-reassign
      },
    });
  }

  function abortRequests() {
    inProgress.forEach(requestName => requests[requestName].xhr.abort());
    inProgress = [];
  }

  return { get, sendRequest, abortRequests };
}

export default loadModule;
