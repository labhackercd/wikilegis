import $ from 'jquery';
import loadModule from './load';
import { requests } from '../config';

const load = loadModule();

function formsModule() {
  function sendComment(formEl) {
    const comment = formEl.text.value;
    const data = {comment: comment};
    if (comment) {
      const $container = $(formEl).closest('[data-collapsible-content]');
      const commentWrapperEl = $container.closest('[data-segment-comments]')[0];
      const segmentId = commentWrapperEl.dataset.segmentComments;

      requests.newComment.wrapperEl = $container.find('[data-comments-list]')[0];
      requests.newComment.path = `render/segment_comments/${segmentId}/segment/`;
      load.post(segmentId, requests.newComment, data);

      requests.newComment.xhr.done((xhr) => {
        commentWrapperEl.style.height = `${$container.outerHeight()}px`;
        formEl.reset();
      });

    } else {
      alert('Favor comentar alguma coisa :)')
    }
  }

  return { sendComment };
}

export default formsModule;
