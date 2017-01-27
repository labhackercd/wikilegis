function tabsModule() {
  let tabContentEl = '';

  function setActiveOnRequestCompletion(elementQuery, index, request) {
    request.xhr.done(() => {
      tabContentEl = document.querySelector(elementQuery);
      tabContentEl.dataset.tabContent = index;
    });
  }

  function setActive(elementQuery, index, request = {}) {
    tabContentEl = document.querySelector(elementQuery);

    if (!tabContentEl) {
      setActiveOnRequestCompletion(elementQuery, index, request);
    } else {
      tabContentEl.dataset.tabContent = index;
    }
  }

  return {
    setActive,
  };
}

export default tabsModule;
