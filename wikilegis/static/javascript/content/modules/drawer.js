/* global segmentsList */
import List from 'list.js';
import $ from 'jquery';
import loadModule from './load';
import { addMultiplePaths, addPath, removePath } from '../utils/history';
import { contents, requests } from '../config';

const load = loadModule();

function drawerModule() {
  function close(contentName, updateHistory = true) {
    const content = contents[contentName];

    if (!content.animating) {
      content.animating = true;
      if (updateHistory) removePath(contentName);
      load.abortRequests();

      content.lastActiveId = content.activeId;
      content.wrapperEl.dataset[`${contentName}Open`] = 'false';
      content.activeId = 0;

      if (contentName === 'bill') close('amendments');
      if (content.wrapperEl.dataset.amendmentsOpen) {
        requests.amendments.loadedIds = [];
      }
      content.animating = false;
    }
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

    if (!content.animating) {
      content.animating = true;

      // specific to bill and amendments
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

        // specific to bill and amendments
        if (contentName === 'bill' && contents.amendments.activeId) close('amendments');
      }

      content.wrapperEl.dataset[`${contentName}Open`] = 'true';
      content.activeId = contentId;

      Object.keys(requests).forEach((request) => {
        let contentRequest = null;
        if (requests[request].content === contentName) {
          contentRequest = requests[request];
        }

        if (contentRequest) {
          const sections = contentRequest.wrapperEl.querySelectorAll('[data-remove-content]');
          sections.forEach((el) => {
            el.parentNode.removeChild(el);
          });
          let callback = () => {
            content.animating = false;
          };
          if (contentName === 'bill' && requests[request].name === 'content') {
            callback = () => {
              const segmentsOptions = {
                searchClass: 'search__input',
                listClass: 'content__segments',
                valueNames: ['segment__text'],
              };
              const billsListSearch = new List('segment-list-search', segmentsOptions);
              segmentsList = billsListSearch; // eslint-disable-line no-global-assign
              content.animating = false;
            };
          }
          load.get(contentId, contentRequest, null, callback);
        }
      });
    }
  }

  return { close, open };
}

export default drawerModule;
