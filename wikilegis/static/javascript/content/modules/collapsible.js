import loadModule from './load';
import content from '../config';

const load = loadModule();

function collapsibleModule() {
  let name = '';
  let request = {};
  let id = 0;
  let isOpen = '';
  let contentEl = {};
  let wrapperEl = {};

  function openOnRequestCompletion() {
    request.xhr.done(() => {
      contentEl = wrapperEl.querySelector('[data-collapsible-content]');
      wrapperEl.style.height = `${contentEl.offsetHeight}px`;
    });
  }

  function open() {
    wrapperEl.dataset.collapsibleOpen = 'true';
    contentEl = wrapperEl.querySelector('[data-collapsible-content]');

    const contentIsLoaded = request.loadedIds.indexOf(id) !== -1;

    if (!contentIsLoaded) {
      load.get(id, request);
    }

    if (!contentEl) {
      openOnRequestCompletion();
    } else {
      wrapperEl.style.height = `${contentEl.offsetHeight}px`;
    }
  }

  function close() {
    wrapperEl.dataset.collapsibleOpen = 'false';
    wrapperEl.style.height = '0';
  }

  function setConfig(targetEl) {
    name = targetEl.dataset.collapsible;
    id = targetEl.dataset[name];

    Object.keys(content).forEach((item) => {
      if (content[item].requests[name]) request = content[item].requests[name];
    });

    const wrapperElQuery = `[data-collapsible-wrapper="${name}"][data-${name}="${id}"]`;
    request.wrapperEl = document.querySelector(wrapperElQuery);
    wrapperEl = request.wrapperEl;

    isOpen = request.wrapperEl.dataset.collapsibleOpen;
  }

  function toggle(targetEl) {
    setConfig(targetEl);

    if (isOpen === 'false') open();
    else close();
  }

  return { toggle };
}

export default collapsibleModule;
