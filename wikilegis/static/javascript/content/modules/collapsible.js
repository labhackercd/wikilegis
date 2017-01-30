import loadModule from './load';
import content from '../config';

const load = loadModule();

function collapsibleModule() {
  let name = '';
  let isOpen = '';
  let request = {};
  let contentEl = {};
  let wrapperEl = {};
  let id = 0;
  let isLoaded = false;

  function setConfig(targetEl) {
    name = targetEl.dataset.collapsible;
    id = targetEl.dataset[name];
    request = content[name].requests[name];
    isLoaded = request.loadedIds.indexOf(id) > -1;

    const wrapperElQuery = `[data-collapsible-wrapper="${name}"][data-${name}="${id}"]`;
    request.wrapperEl = document.querySelector(wrapperElQuery);

    wrapperEl = request.wrapperEl;
    isOpen = wrapperEl.dataset.collapsibleOpen;
  }

  function open() {
    wrapperEl.dataset.collapsibleOpen = 'true';

    if (!isLoaded) {
      load.get(id, request);
      request.xhr.done(() => {
        contentEl = wrapperEl.querySelector('[data-collapsible-content]');
        wrapperEl.style.height = `${contentEl.offsetHeight}px`;
      });
    } else {
      contentEl = wrapperEl.querySelector('[data-collapsible-content]');
      wrapperEl.style.height = `${contentEl.offsetHeight}px`;
    }
  }

  function close() {
    wrapperEl.dataset.collapsibleOpen = 'false';
    wrapperEl.style.height = '0';
  }

  function toggle(targetEl) {
    setConfig(targetEl);

    if (isOpen === 'false') {
      open();
    } else {
      close();
    }
  }

  return { toggle };
}

export default collapsibleModule;
