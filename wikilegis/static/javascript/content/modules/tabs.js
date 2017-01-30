import content from '../config';

function tabsModule() {
  let name = '';
  let contentElQuery = '';
  let contentEl = {};
  let request = {};
  let id = 0;
  let index = 0;
  let isLoaded = false;

  function setConfig(targetEl) {
    name = targetEl.dataset.tabContent;
    index = targetEl.dataset.tab;
    request = content[name].requests[name];
    isLoaded = request.loadedIds.indexOf(id) > -1;
    id = targetEl.dataset[name] ? targetEl.dataset[name] : content[name].activeId;
    contentElQuery = `[data-tab][data-content="${name}"][data-${name}="${id}"]`;
  }

  function setActive(targetEl) {
    setConfig(targetEl);

    if (!isLoaded) {
      request.xhr.done(() => {
        contentEl = document.querySelector(contentElQuery);
        contentEl.dataset.tab = index;
      });
    } else {
      contentEl = document.querySelector(contentElQuery);
      contentEl.dataset.tab = index;
    }
  }

  return { setActive };
}

export default tabsModule;
