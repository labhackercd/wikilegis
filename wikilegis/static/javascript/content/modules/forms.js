/* global strings segmentsList */
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

  function serializeForm(formEl) {
    const data = {};
    const formData = formEl.elements;
    for (let i = formData.length - 1; i >= 0; i -= 1) {
      if (!formData[i].disabled && formData[i].name) {
        if (formData[i].type === 'radio' && formData[i].checked) {
          data[formData[i].name] = formData[i].value;
        } else if (formData[i].type !== 'radio') {
          data[formData[i].name] = formData[i].value;
        }
      }
    }
    return data;
  }

  function sendAmendment(formEl) {
    const segmentContainer = $(formEl).closest('[data-segment-content]')[0];
    const segmentContent = segmentContainer.dataset.segmentContent;
    const amendmentContent = formEl.content.value;

    if (amendmentContent.length === 0 || !amendmentContent.trim()) {
      showAlert(strings.emptyAmendmentTitle, strings.emptyAmendmentText, 'error');
    } else if (segmentContent !== amendmentContent) {
      const data = serializeForm(formEl);
      const parent = $(formEl).closest('[data-segment-id]')[0];
      const parentDataset = parent.dataset;
      const wrapperEl = parent.querySelector('[data-amendments-wrapper]');
      const segmentType = parentDataset.objectType;

      requests.newModifierAmendment.wrapperEl = wrapperEl;
      requests.newModifierAmendment.path = `render/new_amendment/${parentDataset.segmentId}/${segmentType}/`;
      load.sendRequest('post', requests.newModifierAmendment, data);

      requests.newModifierAmendment.xhr.done(() => {
        formEl.reset();

        if (segmentType === 'additive') {
          wrapperEl.previousElementSibling.innerText = '';
        }

        if (segmentType === 'modifier') {
          const segmentDiffWrapper = segmentContainer.querySelector('[data-diff-wrapper]');
          segmentDiffWrapper.innerHTML = segmentContent;
          amendmentDiff.loadDiff(segmentContainer);
        }
      });
    } else {
      showAlert(strings.sameAsSegmentTitle, strings.sameAsSegmentText, 'error');
    }
  }

  function sendSubscribe(formEl) {
    requests.subscribe.wrapperEl = formEl.querySelector('[data-subscribe-wrapper]');
    requests.subscribe.path = formEl.dataset.subscribeUrl;
    const data = serializeForm(formEl);
    load.sendRequest('post', requests.subscribe, data, 'replace');
  }

  function loadSegmentText(inputEl) {
    const segmentContent = $(inputEl).closest('[data-segment-content]')[0];
    if (!inputEl.value) {
      const dataset = segmentContent.dataset;
      inputEl.value = dataset.segmentContent; // eslint-disable-line no-param-reassign
    }
  }

  function segmentSearch(inputEl) {
    if (segmentsList) {
      segmentsList.search(inputEl.value);
    }
  }

  function toggle(form) {
    const wrapperEl = document.querySelector('[data-form-visible]');
    wrapperEl.dataset.formVisible = form;

    const navWrapper = document.querySelector('[data-nav-wrapper]');
    if (form) {
      const textHeight = document.querySelector('[data-nav-text]').offsetHeight;
      navWrapper.style.marginTop = `-${textHeight + 1}px`;
    } else {
      navWrapper.removeAttribute('style');
    }
  }

  return { sendComment, sendAmendment, loadSegmentText, sendSubscribe, segmentSearch, toggle };
}

export default formsModule;
