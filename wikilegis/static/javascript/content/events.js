import { paths } from './config';
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

function changeContent(pathsDiff, action) {
  const pathsDiffArray = pathsDiff.split('/').filter(value => value.trim() !== '');

  for (let i = 0; i < pathsDiffArray.length; i += 2) {
    const contentName = pathsDiffArray[i];
    const contentId = pathsDiffArray[i + 1];

    if (action === 'open') drawer.open(contentName, contentId, false);
    else if (action === 'close') drawer.close(contentName, false);
  }
}

function historyChangeEvent() {
  paths.update(window.location.pathname);

  const pathsLast = paths.last;
  const pathsCurrent = paths.current;
  let pathsDiff = '';

  if (pathsCurrent === '/') {
    pathsDiff = pathsLast;
    changeContent(pathsDiff, 'close');
  } else if (pathsLast === '/') {
    pathsDiff = pathsCurrent;
    changeContent(pathsDiff, 'open');
  } else if (pathsCurrent > pathsLast) {
    pathsDiff = pathsCurrent.replace(pathsLast, '');
    changeContent(pathsDiff, 'open');
  } else if (pathsCurrent < pathsLast) {
    pathsDiff = pathsLast.replace(pathsCurrent, '');
    changeContent(pathsDiff, 'close');
  }
}

document.addEventListener('click', clickEvent);
window.onpopstate = historyChangeEvent;
