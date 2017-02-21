import { paths } from './config';
import { updatePath, updateHash } from './utils/history';
import collapsibleModule from './modules/collapsible';
import drawerModule from './modules/drawer';
import hoverModule from './modules/hover';
import tabsModule from './modules/tabs';
import formsModule from './modules/forms';
import votesModule from './modules/votes';

const collapsible = collapsibleModule();
const drawer = drawerModule();
const hover = hoverModule();
const tabs = tabsModule();
const forms = formsModule();
const votes = votesModule();

function clickEvent(event) {
  const dataset = event.target.dataset;
  const parent = event.target.closest('[data-drawer-open], [data-vote-action]');
  let parentDataset = null;
  if (parent) {
    parentDataset = parent.dataset;
  }


  if (dataset.drawerOpen) {
    drawer.open(event.target);
  } else if (parentDataset && parentDataset.drawerOpen) {
    drawer.open(parent);
  } else if (dataset.drawerClose) {
    drawer.close(dataset.drawerClose);
  }

  if (dataset.voteAction) {
    votes.sendVote(event.target);
  } else if (parentDataset && parentDataset.voteAction) {
    votes.sendVote(parent);
  }

  if (dataset.tab && dataset.drawerOpen) {
    updatePath(event.target.href);
  } else if (dataset.tab) {
    updateHash(event.target.href, event.target.hash);
  }

  if (dataset.collapsible) {
    collapsible.toggle(event.target);
  }
}

function mouseoverEvent(event) {
  if (event.target.dataset.hover === 'segment-add') {
    hover.showSegmentAdd(event.target);
  }
}

function mouseoutEvent(event) {
  if (event.target.dataset.hover === 'segment-add') {
    hover.hideSegmentAdd(event.target);
  }
}

function submitEvent(event) {
  event.preventDefault();
  const dataset = event.target.dataset;

  if ('commentsForm' in dataset) {
    forms.sendComment(event.target);
  }

  if ('amendmentsForm' in dataset) {
    forms.sendAmendment(event.target);
  }
}

function focusEvent(event) {
  const dataset = event.target.dataset;

  if ('amendmentsInput' in dataset) {
    forms.loadSegmentText(event.target);
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

  const hash = window.location.hash;
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

  // specific to tab
  if (hash.indexOf('tab_') > -1) {
    const navItemEl = document.querySelector(`.nav__item[data-tab][href="${hash}"]`);
    tabs.setActive(navItemEl);
  }
}

function windowLoadEvent() {
  const hash = window.location.hash;

  changeContent(window.location.pathname, 'open');

  // specific to tab
  if (hash.indexOf('tab_') > -1) {
    const navItemEl = document.querySelector(`.nav__item[data-tab][href="${hash}"]`);
    tabs.setActive(navItemEl);
  }
}

document.addEventListener('click', clickEvent);
document.addEventListener('mouseover', mouseoverEvent);
document.addEventListener('mouseout', mouseoutEvent);
document.addEventListener('submit', submitEvent);
document.addEventListener('focus', focusEvent, true);

window.onpopstate = historyChangeEvent;
window.onload = windowLoadEvent;
