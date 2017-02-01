import loadModule from './load';
import { requests } from '../config';

const load = loadModule();

function collapsibleModule() {
  let name = '';
  let isOpen = '';
  let request = {};
  let triggerEl = {};
  let wrapperEl = {};
  let id = 0;
  let isLoaded = false;

  function setConfig(targetEl) {
    name = targetEl.dataset.collapsible;
    id = targetEl.dataset[name];
    request = requests[name];
    triggerEl = targetEl;
    isLoaded = request.loadedIds.indexOf(id) > -1;

    const wrapperElQuery = `[data-collapsible-wrapper="${name}"][data-${name}="${id}"]`;
    request.wrapperEl = document.querySelector(wrapperElQuery);

    wrapperEl = request.wrapperEl;
    isOpen = triggerEl.dataset.collapsibleOpen;
  }

  function open() {
    triggerEl.dataset.collapsibleOpen = 'true';

    if (!isLoaded) {
      load.get(id, request);
      request.xhr.done(() => {
        const contentEl = wrapperEl.querySelector('[data-collapsible-content]');
        wrapperEl.style.height = `${contentEl.offsetHeight}px`;
      });
    } else {
      const contentEl = wrapperEl.querySelector('[data-collapsible-content]');
      wrapperEl.style.height = `${contentEl.offsetHeight}px`;
    }
  }

  function close() {
    triggerEl.dataset.collapsibleOpen = 'false';
    wrapperEl.style.height = '0';
  }

  function toggle(targetEl) {
    setConfig(targetEl);

    if (isOpen === 'false') open();
    else close();
  }

  return { toggle };
}

export default collapsibleModule;
