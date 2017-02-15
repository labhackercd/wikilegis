import $ from 'jquery';
import { requests } from '../config';

function loadModule() {
  let inProgress = [];

  function setLoader(wrapperEl, loading) {
    const loaderEl = wrapperEl.getElementsByClassName('loader')[0];
    loaderEl.dataset.loading = loading;
  }

  function get(id, request, param) {
    const pathParam = !param ? id : param;
    const path = request.path;
    const url = `/${path}${pathParam}`;

    $.ajax({
      url,
      beforeSend(xhr) {
        request.xhr = xhr; // eslint-disable-line no-param-reassign
        inProgress.push(request.name);
        setLoader(request.wrapperEl, true);
      },
      success(xhr) {
        request.wrapperEl.insertAdjacentHTML('beforeend', xhr.html);
        request.loadedIds.push(id);
      },
      error(xhr, status) {
        console.log(status); // eslint-disable-line no-console
      },
      complete() {
        const requestIndex = inProgress.indexOf(request.name);
        if (requestIndex > -1) inProgress.splice(requestIndex, 1);
        request.xhr = {}; // eslint-disable-line no-param-reassign
        setLoader(request.wrapperEl, false);
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

  function post(id, request, data) {
    const path = request.path;
    const url = `/${path}`;

    $.ajax({
      url,
      type: 'POST',
      data,
      beforeSend(xhr) {
        if (!this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', getCSRF());
        }
        request.xhr = xhr; // eslint-disable-line no-param-reassign
      },
      success(xhr) {
        request.wrapperEl.insertAdjacentHTML('beforeend', xhr.html);
      },
      error(xhr, status) {
        console.log(status); // eslint-disable-line no-console
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

  return { get, post, abortRequests };
}

export default loadModule;
