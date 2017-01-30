import drawerModule from './modules/drawer';
import tabsModule from './modules/tabs';
import collapsibleModule from './modules/collapsible';

import content from './config';

const drawer = drawerModule();
const tabs = tabsModule();
const collapsible = collapsibleModule();

function clickEvent(event) {
  const dataset = event.target.dataset;

  if (dataset.drawerOpen) {
    const contentName = dataset.drawerOpen;
    const contentId = dataset[contentName];

    drawer.open(contentName, contentId);
  } else if (dataset.drawerClose) {
    drawer.close(dataset.drawerClose);
  }

  if (dataset.collapsible) {
    if (dataset.comments) {
      const commentsRequest = content.comments.requests.comments;
      const commentsId = dataset.comments;
      const collapsibleWrapperEl = document.querySelector(`[data-collapsible-wrapper][data-comments="${commentsId}"]`);
      const collapsibleContentElQuery = '[data-collapsible-content]';

      commentsRequest.wrapperEl = collapsibleWrapperEl;

      if (collapsibleWrapperEl.dataset.collapsibleOpen === 'false') {
        collapsible.open(collapsibleContentElQuery, commentsId, commentsRequest);
      } else {
        collapsible.close(collapsibleContentElQuery, commentsId, commentsRequest);
      }
    }
  }

  if (dataset.tab) {
    const tabIndex = dataset.tab;

    if (dataset.interactions) {
      const tabContentElQuery = `[data-tab-content][data-interactions="${dataset.interactions}"]`;
      const tabRequest = content.interactions.requests.interactions;

      tabs.setActive(tabContentElQuery, tabIndex, tabRequest);
    } else if (content.interactions.activeId) {
      const tabContentElQuery = `[data-tab-content][data-interactions="${content.interactions.activeId}"]`;

      tabs.setActive(tabContentElQuery, tabIndex);
    }
  }
}

document.addEventListener('click', clickEvent);
