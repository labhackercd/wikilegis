import $ from 'jquery';
import loadModule from './load';
import { addMultiplePaths, addPath, removePath } from '../utils/history';
import { contents, requests } from '../config';

const load = loadModule();

function drawerModule() {
  function close(contentName, updateHistory = true) {
    const content = contents[contentName];

    if (updateHistory) removePath(contentName);
    load.abortRequests();

    content.lastActiveId = content.activeId;
    content.wrapperEl.dataset[`${contentName}Open`] = 'false';
    content.activeId = 0;
  }

  function open(...args) {
    let contentName = '';
    let contentId = 0;
    let updateHistory = true;

    if (args.length === 1) { // targetEl
      contentName = args[0].dataset.drawerOpen;
      contentId = args[0].dataset[contentName];
    } else if (args.length === 2) { // name, id
      contentName = args[0];
      contentId = args[1];
    } else { // name, id, updateHistory
      contentName = args[0];
      contentId = args[1];
      updateHistory = args[2];
    }

    const content = contents[contentName];

    // specific to bill and iteractions
    if (updateHistory) {
      if (content.lastActiveId === contentId && contentName === 'bill' && contents.amendments.activeId) {
        addMultiplePaths(contentName, contentId, 'amendments', contents.amendments.activeId);
      } else {
        addPath(contentName, contentId);
      }
    }

    const $active = $(`[data-content="${contentName}"][data-${contentName}="${contentId}"]`);
    $active.removeClass('hidden');

    if (content.lastActiveId !== contentId) {
      const $lastActiveContent = $(`[data-content="${contentName}"][data-${contentName}="${content.lastActiveId}"]`);
      $lastActiveContent.addClass('hidden');

      // specific to bill and iteractions
      if (contentName === 'bill' && contents.amendments.activeId) close('amendments');
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
