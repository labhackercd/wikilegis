const wikilegisEl = document.getElementsByClassName('wikilegis')[0];
const billInfoWrapperEl = document.getElementsByClassName('bill__info-wrapper')[0];
const billContentWrapperEl = document.getElementsByClassName('bill__content-wrapper')[0];
const billAmendmentsWrapperEl = document.getElementsByClassName('bill__amendments-wrapper')[0];
const billAmendmentSegmentWrapperEl = document.getElementsByClassName('amendment__text-wrapper')[0];

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
contents.amendments = new Content('amendments', billAmendmentsWrapperEl);
contents.comments = new Content('comments');
contents.widget = new Content('widget', billContentWrapperEl);

const requests = {};
requests.info = new Request('bill', 'info', billInfoWrapperEl, 'render/bill_info/');
requests.content = new Request('bill', 'content', billContentWrapperEl, 'render/bill_content/');
requests.amendments = new Request('amendments', 'amendments', billAmendmentsWrapperEl, 'render/bill_amendments/');
requests.amendmentSegment = new Request('amendments', 'amendmentSegment', billAmendmentSegmentWrapperEl, 'render/bill_amendment_segment/');
requests.amendmentComments = new Request('comments', 'comments', undefined, 'render/amendment_comments/');
requests.segmentComments = new Request('comments', 'comments', undefined, 'render/segment_comments/');
requests.newComment = new Request('comments', 'comments', undefined, '');
requests.votes = new Request('votes', 'votes', undefined, '');
requests.newModifierAmendment = new Request('modifierAmendments', 'modifierAmendments', undefined, '');
requests.subscribe = new Request('subscribe', 'subscribe', undefined, '');

const paths = new Path();

export { contents, requests, paths };
