import $ from 'jquery';
import { contents, requests } from '../config';
import amendmentDiffModule from './amendmentDiff';

const amendmentDiff = amendmentDiffModule();

function tabsModule() {
  function setActive(targetEl) {
    const name = targetEl.dataset.tabContent;
    const index = targetEl.dataset.tab;
    const tabContentType = targetEl.dataset.tabContentType;
    const request = requests[name];
    const id = targetEl.dataset[name] ? targetEl.dataset[name] : contents[name].activeId;
    const isLoaded = request.loadedIds.indexOf(id) > -1;
    const contentElQuery = `[data-tab][data-content="${name}"][data-${name}="${id}"]`;
    const contentEl = contents[name].wrapperEl.querySelector(contentElQuery);
    const targetParentEl = targetEl.parentElement;

    if (!isLoaded) {
      request.xhr.done(() => {
        contents[name].wrapperEl.querySelector(contentElQuery).dataset.tab = index;
        targetParentEl.dataset.tab = index;
        const modifierAmendmentsWrapperEl = contents[name].wrapperEl.querySelector('[data-object-type=modifier]');
        amendmentDiff.loadDiff(modifierAmendmentsWrapperEl);
      });
    } else {
      contents[name].wrapperEl.querySelector(contentElQuery).dataset.tab = index;
      targetParentEl.dataset.tab = index;
    }

    const amendmentsWrapperEl = document.querySelector('[data-amendments-container]')

    amendmentsWrapperEl.dataset.formVisible = 'false';
    amendmentsWrapperEl.dataset.currentTab = tabContentType;
    document.querySelectorAll('[data-form-open]').forEach((buttonEl) => {
      $(buttonEl).removeClass('animate');
      // setTimeout needed for the button animation to re-fire on the first tab change. Pls don't judge.
      setTimeout(() => {
        if (tabContentType === buttonEl.dataset.formOpen) {
          $(buttonEl).addClass('animate');
          amendmentsWrapperEl.dataset.currentTab = tabContentType;
        }
      }, 100)
    })

  }

  return { setActive };
}

export default tabsModule;
