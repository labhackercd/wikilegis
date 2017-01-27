import $ from 'jquery';
import loadModule from './load';
import content from '../config';

const load = loadModule();

function drawerModule() {
  function close(contentName) {
    const contentObj = content[contentName];

    load.abortRequests(contentObj);

    contentObj.lastActiveId = contentObj.activeId;
    contentObj.wrapperEl.dataset[`${contentName}Open`] = 'false';
    contentObj.activeId = 0;
  }

  function open(contentName, contentId) {
    const contentObj = content[contentName];
    const requests = contentObj.requests;

    const $active = $(`[data-content="${contentName}"][data-${contentName}="${contentId}"]`);
    $active.removeClass('hidden');

    if (contentObj.lastActiveId !== contentId) {
      const $lastActiveContent = $(`[data-content="${contentName}"][data-${contentName}="${contentObj.lastActiveId}"]`);
      $lastActiveContent.addClass('hidden');

      if (contentName === 'bill') close('interactions');
    }

    contentObj.wrapperEl.dataset[`${contentName}Open`] = 'true';
    contentObj.activeId = contentId;

    Object.keys(requests).forEach((request) => {
      if (requests[request].loadedIds.indexOf(contentId) === -1) {
        load.get(contentId, contentObj.requests[request]);
      }
    });
  }

  return {
    close,
    open,
  };
}

export default drawerModule;
