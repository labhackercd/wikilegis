import $ from 'jquery';
import loadModule from './load';
import { requests } from '../config';
import { hasClass } from '../utils/polyfills';

const load = loadModule();


function votesModule() {
  function sendVote(voteActionEl) {
    const vote = JSON.parse(voteActionEl.dataset.voteAction);
    const data = { vote };
    const voteWrapperEl = $(voteActionEl).closest('[data-votes-wrapper]')[0];
    const segmentType = $(voteWrapperEl).closest('[data-object-type]')[0].dataset.objectType;

    requests.votes.path = `render/vote/${voteWrapperEl.dataset.objectId}/${segmentType}/`;
    requests.votes.wrapperEl = voteWrapperEl;
    if (hasClass(voteActionEl, 'voted')) {
      load.sendRequest('post', requests.votes, data, 'replace');
    } else {
      load.sendRequest('post', requests.votes, data, 'replace');
    }
  }

  return { sendVote };
}

export default votesModule;
