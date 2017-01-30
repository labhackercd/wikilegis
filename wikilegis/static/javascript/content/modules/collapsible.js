import loadModule from './load';

const load = loadModule();

function collapsibleModule() {
  let collapsibleContentEl;

  function openOnRequestCompletion(elementQuery, index, request) {
    request.xhr.done(() => {
      collapsibleContentEl = request.wrapperEl.querySelector(elementQuery);
      request.wrapperEl.style.height = `${collapsibleContentEl.offsetHeight}px`;
    });
  }

  function open(elementQuery, id, request) {
    request.wrapperEl.dataset.collapsibleOpen = 'true';

    if (request.loadedIds.indexOf(id) === -1) {
      load.get(id, request);
    }

    collapsibleContentEl = request.wrapperEl.querySelector(elementQuery);

    if (!collapsibleContentEl) {
      openOnRequestCompletion(elementQuery, id, request);
    } else {
      request.wrapperEl.style.height = `${collapsibleContentEl.offsetHeight}px`;
    }
  }

  function close(elementQuery, id, request) {
    request.wrapperEl.dataset.collapsibleOpen = 'false';
    request.wrapperEl.style.height = '0';
  }

  return {
    open,
    close,
  };
}

export default collapsibleModule;
