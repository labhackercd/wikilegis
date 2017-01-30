import drawerModule from './modules/drawer';
import tabsModule from './modules/tabs';
import collapsibleModule from './modules/collapsible';

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
    collapsible.toggle(event.target);
  }

  if (dataset.tab) {
    tabs.setActive(event.target);
  }
}

document.addEventListener('click', clickEvent);
