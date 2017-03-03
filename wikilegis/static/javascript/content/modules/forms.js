import $ from 'jquery';
import loadModule from './load';
import amendmentDiffModule from './amendmentDiff';
import { showAlert } from '../utils/alert';
import { requests } from '../config';

const amendmentDiff = amendmentDiffModule();
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
      showAlert(strings.emptyCommentTitle, strings.emptyCommentText, 'error');
    }
  }

  function sendAmendment(formEl) {
    const segmentContainer = $(formEl).closest('[data-segment-content]')[0];
    const segmentContent = segmentContainer.dataset.segmentContent;
    const amendmentContent = formEl.text.value;
    if (amendmentContent.length === 0 || !amendmentContent.trim()) {
      showAlert(strings.emptyAmendmentTitle, strings.emptyAmendmentText, 'error');
    } else if (segmentContent !== amendmentContent) {
      const data = {
        content: amendmentContent,
      };
      const parentDataset = formEl.parentNode.dataset;
      const wrapperEl = formEl.parentNode.querySelector('[data-amendments-wrapper]');
      const segmentType = parentDataset.objectType;

      requests.newModifierAmendment.wrapperEl = wrapperEl;
      requests.newModifierAmendment.path = `render/new_amendment/${parentDataset.segmentId}/${segmentType}/`;
      load.sendRequest('post', requests.newModifierAmendment, data);

      requests.newModifierAmendment.xhr.done(() => {
        formEl.reset();
        const segmentDiffWrapper = segmentContainer.querySelector('[data-diff-wrapper]');
        segmentDiffWrapper.innerHTML = segmentContent;
        amendmentDiff.loadDiff(segmentContainer);
      });
    } else {
      showAlert(strings.sameAsSegmentTitle, strings.sameAsSegmentText, 'error');
    }
  }

  function loadSegmentText(inputEl) {
    const segmentContent = $(inputEl).closest('[data-segment-content]')[0];
    if (!inputEl.value) {
      const dataset = segmentContent.dataset;
      inputEl.value = dataset.segmentContent; // eslint-disable-line no-param-reassign
    }
  }

  return { sendComment, sendAmendment, loadSegmentText };
}

export default formsModule;
