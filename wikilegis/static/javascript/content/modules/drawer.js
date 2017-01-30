import $ from 'jquery';
import loadModule from './load';
import { contents, requests } from '../config';

const load = loadModule();

function drawerModule() {
  function close(contentName) {
    const content = contents[contentName];

    load.abortRequests();

    content.lastActiveId = content.activeId;
    content.wrapperEl.dataset[`${contentName}Open`] = 'false';
    content.activeId = 0;
  }

  function open(targetEl) {
    const contentName = targetEl.dataset.drawerOpen;
    const contentId = targetEl.dataset[contentName];
    const content = contents[contentName];

    const $active = $(`[data-content="${contentName}"][data-${contentName}="${contentId}"]`);
    $active.removeClass('hidden');

    if (content.lastActiveId !== contentId) {
      const $lastActiveContent = $(`[data-content="${contentName}"][data-${contentName}="${content.lastActiveId}"]`);
      $lastActiveContent.addClass('hidden');

      if (contentName === 'bill') close('interactions'); // specific to bill and iteractions
    }

    content.wrapperEl.dataset[`${contentName}Open`] = 'true';
    content.activeId = contentId;

    Object.keys(requests).forEach((request) => {
      const contentRequest = requests[request].content === contentName ? requests[request] : false;

      if (contentRequest && contentRequest.loadedIds.indexOf(contentId) === -1) {
        load.get(contentId, contentRequest);
      }
    });
  }

  return { close, open };
}

export default drawerModule;
