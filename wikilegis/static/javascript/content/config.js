const wikilegisEl = document.getElementsByClassName('wikilegis')[0];
const billInfoWrapperEl = document.getElementsByClassName('bill__info-wrapper')[0];
const billContentWrapperEl = document.getElementsByClassName('bill__content-wrapper')[0];
const billInteractionsWrapperEl = document.getElementsByClassName('bill__interactions-wrapper')[0];

const content = {
  bill: {
    wrapperEl: wikilegisEl,
    activeId: 0,
    lastActiveId: 0,
    requests: {
      info: {
        name: 'info',
        wrapperEl: billInfoWrapperEl,
        path: 'render/bill_info/',
        loadedIds: [],
        xhr: {},
      },
      content: {
        name: 'content',
        wrapperEl: billContentWrapperEl,
        path: 'render/bill_content/',
        loadedIds: [],
        xhr: {},
      },
    },
  },
  interactions: {
    wrapperEl: billInteractionsWrapperEl,
    activeId: 0,
    lastActiveId: 0,
    requests: {
      interactions: {
        name: 'interactions',
        wrapperEl: billInteractionsWrapperEl,
        path: 'render/bill_interactions/',
        loadedIds: [],
        xhr: {},
      },
    },
  },
  comments: {
    wrapperEl: {},
    activeId: 0,
    lastActiveId: 0,
    requests: {
      comments: {
        name: 'comments',
        wrapperEl: {},
        path: 'render/segment_comments/',
        loadedIds: [],
        xhr: {},
      },
    },
  },
};

export default content;
