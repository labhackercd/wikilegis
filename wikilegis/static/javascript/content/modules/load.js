import $ from 'jquery';

function loadModule() {
  let inProgress = [];

  function setLoader(wrapperEl, loading) {
    const loaderEl = wrapperEl.getElementsByClassName('loader')[0];
    loaderEl.dataset.loading = loading;
  }

  function get(id, request) {
    const locationPath = window.location.pathname;
    const path = request.path;
    const url = locationPath + path + id;

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

  function abortRequests(contentObj) {
    inProgress.forEach((requestName) => {
      contentObj.requests[requestName].xhr.abort();
    });
    inProgress = [];
  }

  return {
    inProgress,
    get,
    abortRequests,
  };
}

export default loadModule;
