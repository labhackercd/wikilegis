import drawerModule from './modules/drawer';
import tabsModule from './modules/tabs';
import collapsibleModule from './modules/collapsible';

const drawer = drawerModule();
const tabs = tabsModule();
const collapsible = collapsibleModule();

function clickEvent(event) {
  const dataset = event.target.dataset;

  if (dataset.drawerOpen) {
    drawer.open(event.target);
  } else if (dataset.drawerClose) {
    drawer.close(dataset.drawerClose);
  }

  if (dataset.tab) {
    tabs.setActive(event.target);
  }

  if (dataset.collapsible) {
    collapsible.toggle(event.target);
  }
}

document.addEventListener('click', clickEvent);
