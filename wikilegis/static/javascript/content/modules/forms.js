import $ from 'jquery';
import loadModule from './load';
import { requests } from '../config';

const load = loadModule();

function formsModule() {
  function sendComment(formEl) {
    const comment = formEl.text.value;
    const data = { comment };
    if (comment) {
      const $container = $(formEl).closest('[data-collapsible-content]');
      const segmentType = $container.closest('[data-object-type]')[0].dataset.objectType;

      let dataAttribute = segmentType;
      if (segmentType !== 'segment') dataAttribute = 'amendment';

      const commentWrapperEl = $container.closest('[data-comments-wrapper]')[0];
      const segmentId = commentWrapperEl.getAttribute(`data-${dataAttribute}-comments`);

      requests.newComment.wrapperEl = $container.find('[data-comments-list]')[0];
      requests.newComment.path = `render/new_comment/${segmentId}/${segmentType}/`;
      load.sendRequest('post', requests.newComment, data);

      requests.newComment.xhr.done(() => {
        commentWrapperEl.style.height = `${$container.outerHeight()}px`;
        formEl.reset();
      });
    } else {
      // TODO: alert user to write something on input
    }
  }

  return { sendComment };
}

export default formsModule;
