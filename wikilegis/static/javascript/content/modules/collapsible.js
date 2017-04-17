import $ from 'jquery';
import loadModule from './load';
import { requests } from '../config';

const load = loadModule();

function collapsibleModule() {
  let name = '';
  let nameCamelCase = '';
  let param = '';
  let isOpen = '';
  let request = {};
  let triggerEl = {};
  let wrapperEl = {};
  let id = 0;
  let isLoaded = false;

  function toCamelCase(string) {
    return string.replace(/-([a-z])/g, char => char[1].toUpperCase());
  }

  function setConfig(targetEl) {
    const dataset = targetEl.dataset;

    name = dataset.collapsible;
    nameCamelCase = toCamelCase(name);
    param = dataset.param;
    id = dataset[nameCamelCase];
    request = requests[nameCamelCase];
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
      load.get(id, request, param);
      request.xhr.done(() => {
        const contentEl = wrapperEl.querySelector('[data-collapsible-content]');
        wrapperEl.style.height = `${$(contentEl).outerHeight(true)}px`;
        wrapperEl.dataset.collapsibleOpen = true;
      });
    } else {
      const contentEl = wrapperEl.querySelector('[data-collapsible-content]');
      wrapperEl.style.height = `${$(contentEl).outerHeight(true)}px`;
      wrapperEl.dataset.collapsibleOpen = true;
    }
  }

  function close() {
    triggerEl.dataset.collapsibleOpen = 'false';
    wrapperEl.style.height = '0';
    wrapperEl.dataset.collapsibleOpen = false;
  }

  function toggle(targetEl) {
    setConfig(targetEl);

    if (isOpen === 'false') open();
    else close();
  }

  return { toggle };
}

export default collapsibleModule;
