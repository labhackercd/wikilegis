import toggleModule from './modules/toggle';
import tabsModule from './modules/tabs';

import content from './config';

const toggle = toggleModule();
const tabs = tabsModule();

function clickEvent(event) {
  const dataset = event.target.dataset;

  if (dataset.show) {
    const contentName = dataset.show;
    const contentId = dataset[contentName];

    toggle.show(contentName, contentId);
  } else if (dataset.hide) {
    toggle.hide(dataset.hide);
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
