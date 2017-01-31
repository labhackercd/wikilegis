const wikilegisEl = document.getElementsByClassName('wikilegis')[0];
const billInfoWrapperEl = document.getElementsByClassName('bill__info-wrapper')[0];
const billContentWrapperEl = document.getElementsByClassName('bill__content-wrapper')[0];
const billInteractionsWrapperEl = document.getElementsByClassName('bill__interactions-wrapper')[0];

class Content {
  constructor(name = '', wrapperEl = {}, activeId = 0, lastActiveId = 0) {
    this.name = name;
    this.wrapperEl = wrapperEl;
    this.activeId = activeId;
    this.lastActiveId = lastActiveId;
  }
}

class Request {
  constructor(content = '', name = '', wrapperEl = {}, path = '', loadedIds = [], xhr = {}) {
    this.content = content;
    this.name = name;
    this.wrapperEl = wrapperEl;
    this.path = path;
    this.loadedIds = loadedIds;
    this.xhr = xhr;
  }
}

class Path {
  constructor(last = '', current = window.location.pathname, hash = '') {
    this.last = last;
    this.current = current;
    this.hash = hash;
  }

  update(current = this.current, hash = this.hash) {
    this.last = this.current;
    this.current = current;
    this.hash = hash;
  }
}

const contents = {};
contents.bill = new Content('bill', wikilegisEl);
contents.interactions = new Content('interactions', billInteractionsWrapperEl);
contents.comments = new Content('comments');

const requests = {};
requests.info = new Request('bill', 'info', billInfoWrapperEl, 'render/bill_info/');
requests.content = new Request('bill', 'content', billContentWrapperEl, 'render/bill_content/');
requests.interactions = new Request('interactions', 'interactions', billInteractionsWrapperEl, 'render/bill_interactions/');
requests.comments = new Request('comments', 'comments', undefined, 'render/segment_comments/');

const paths = new Path();

export { contents, requests, paths };
