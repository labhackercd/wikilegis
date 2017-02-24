import { contents, requests } from '../config';
import amendmentDiffModule from './amendmentDiff';

const amendmentDiff = amendmentDiffModule();

function tabsModule() {
  function setActive(targetEl) {
    const name = targetEl.dataset.tabContent;
    const index = targetEl.dataset.tab;
    const request = requests[name];
    const id = targetEl.dataset[name] ? targetEl.dataset[name] : contents[name].activeId;
    const isLoaded = request.loadedIds.indexOf(id) > -1;
    const contentElQuery = `[data-tab][data-content="${name}"][data-${name}="${id}"]`;
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
  }

  return { setActive };
}

export default tabsModule;
