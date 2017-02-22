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

  function sendAmendment(formEl) {
    const segmentContent = $(formEl).closest('[data-segment-content]')[0].dataset.segmentContent;
    const amendmentContent = formEl.text.value;
    if (amendmentContent.length === 0 || !amendmentContent.trim()) {
      // TODO: suggest user to do a suppress amendment
    } else if (segmentContent !== amendmentContent) {
      const data = {
        content: amendmentContent
      }
      const parentDataset = formEl.parentNode.dataset;
      const wrapperEl = formEl.parentNode.querySelector('[data-amendments-wrapper]');
      const segmentType = parentDataset.objectType;

      requests.newModifierAmendment.wrapperEl = wrapperEl;
      requests.newModifierAmendment.path = `render/new_amendment/${parentDataset.segmentId}/${segmentType}/`;
      load.sendRequest('post', requests.newModifierAmendment, data);

      requests.newModifierAmendment.xhr.done(() => {
        wrapperEl.style.height = `${wrapperEl.offsetHeight}px`;
        formEl.reset();
      });

    } else {
      // TODO: alert user to modify anything on the original text
    }
  }

  function loadSegmentText(inputEl) {
    const segmentContent = $(inputEl).closest('[data-segment-content]')[0];
    if (!inputEl.value) {
      inputEl.value = segmentContent.dataset.segmentContent;
    }
  }

  return { sendComment, sendAmendment, loadSegmentText };
}

export default formsModule;
