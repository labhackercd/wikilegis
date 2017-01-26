import $ from 'jquery';

function toggleContent() {
  const elements = {
    wikilegisEl: document.getElementsByClassName('wikilegis')[0],
    billInfoWrapperEl: document.getElementsByClassName('bill__info-wrapper')[0],
    billContentWrapperEl: document.getElementsByClassName('bill__content-wrapper')[0],
    billInteractionsWrapperEl: document.getElementsByClassName('bill__interactions-wrapper')[0],
  };

  const content = {
    bill: {
      wrapperEl: elements.wikilegisEl,
      activeId: 0,
      lastActiveId: 0,
      requests: {
        info: {
          name: 'info',
          wrapperEl: elements.billInfoWrapperEl,
          path: 'render/bill_info/',
          loadedIds: [],
          xhr: {},
        },
        content: {
          name: 'content',
          wrapperEl: elements.billContentWrapperEl,
          path: 'render/bill_content/',
          loadedIds: [],
          xhr: {},
        },
      },
    },
    interactions: {
      wrapperEl: elements.billInteractionsWrapperEl,
      activeId: 0,
      lastActiveId: 0,
      requests: {
        interactions: {
          name: 'interactions',
          wrapperEl: elements.billInteractionsWrapperEl,
          path: 'render/bill_interactions/',
          loadedIds: [],
          xhr: {},
        },
      },
    },
  };

  let ajaxRequests = [];

  function setLoader(request, loading) {
    const loaderEl = request.wrapperEl.getElementsByClassName('loader')[0];
    loaderEl.dataset.loading = loading;
  }

  function getContent(id, request) {
    const locationPath = window.location.pathname;
    const path = request.path;
    const url = locationPath + path + id;

    $.ajax({
      url,
      beforeSend(xhr) {
        request.xhr = xhr; // eslint-disable-line no-param-reassign
        ajaxRequests.push(request.name);
        setLoader(request, true);
      },
      success(xhr) {
        request.wrapperEl.insertAdjacentHTML('beforeend', xhr.html);
        request.loadedIds.push(id);
      },
      error(xhr, status) {
        console.log(status); // eslint-disable-line no-console
      },
      complete() {
        const requestIndex = ajaxRequests.indexOf(request.name);
        if (requestIndex > -1) ajaxRequests.splice(requestIndex, 1);
        request.xhr = {}; // eslint-disable-line no-param-reassign
        setLoader(request, false);
      },
    });
  }

  function abortAjaxRequests(contentData) {
    ajaxRequests.forEach((requestName) => {
      contentData.requests[requestName].xhr.abort();
    });
    ajaxRequests = [];
  }

  function removeActiveContent(contentName) {
    const contentObj = content[contentName];

    abortAjaxRequests(contentObj);

    contentObj.lastActiveId = contentObj.activeId;
    contentObj.wrapperEl.dataset[`${contentName}Open`] = 'false';
    contentObj.activeId = 0;
  }

  function showActiveContent(contentName, contentId) {
    const contentObj = content[contentName];
    const requests = contentObj.requests;

    const $activeContent = $(`[data-content="${contentName}"][data-${contentName}="${contentId}"]`);

    if (contentObj.lastActiveId !== contentId) {
      const $lastActiveContent = $(`[data-content="${contentName}"][data-${contentName}="${contentObj.lastActiveId}"]`);

      $lastActiveContent.addClass('hidden');
      removeActiveContent('interactions');
    }

    $activeContent.removeClass('hidden');
    contentObj.wrapperEl.dataset[`${contentName}Open`] = 'true';
    contentObj.activeId = contentId;

    Object.keys(requests).forEach((request) => {
      if (requests[request].loadedIds.indexOf(contentId) === -1) {
        getContent(contentId, contentObj.requests[request]);
      }
    });
  }

  function toggleInteractionsContent(index) {
    const activeId = content.interactions.activeId;

    if (ajaxRequests.indexOf('interactions') > -1) {
      content.interactions.requests.interactions.xhr.done(() => {
        const interactionsEl = elements.billInteractionsWrapperEl.querySelector(`[data-interactions="${activeId}"]`);
        interactionsEl.dataset.interactionsContent = index;
      });
    } else {
      const interactionsEl = elements.billInteractionsWrapperEl.querySelector(`[data-interactions="${activeId}"]`);
      interactionsEl.dataset.interactionsContent = index;
    }
  }

  function clickEvent(event) {
    const dataset = event.target.dataset;

    if (dataset.open) {
      const contentName = dataset.open;
      const contentId = dataset[contentName];

      showActiveContent(contentName, contentId);
    }

    if (dataset.close) {
      removeActiveContent(dataset.close);
    }

    if (dataset.interactionsNav) {
      toggleInteractionsContent(dataset.interactionsNav);
    }
  }

  elements.wikilegisEl.addEventListener('click', clickEvent);
}

export default toggleContent;
