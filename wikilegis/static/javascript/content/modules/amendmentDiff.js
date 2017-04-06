import $ from 'jquery';

const diff = require('diff');

function amendmentDiffModule() {
  function buildMarkup(oldText, newText) {
    const diffElement = document.createDocumentFragment();
    diff.diffWordsWithSpace(oldText, newText).forEach((part) => {
      let className = '';
      if (part.added) className = 'diff-added';
      else if (part.removed) className = 'diff-removed';

      const span = document.createElement('span');
      $(span).addClass(className);
      span.appendChild(document.createTextNode(part.value));
      diffElement.appendChild(span);
    });
    return diffElement;
  }

  function updateDiff(inputEl) {
    const containerEL = $(inputEl).closest('[data-segment-content]')[0];
    const segmentContent = containerEL.dataset.segmentContent;
    const diffEl = buildMarkup(segmentContent, inputEl.value);

    const diffWrapperEl = containerEL.querySelector('[data-diff-wrapper]');
    diffWrapperEl.innerHTML = '';
    diffWrapperEl.appendChild(diffEl);
  }

  function loadDiff(amendmentsWrapperEl) {
    const amendments = amendmentsWrapperEl.querySelectorAll('[data-amendment-content]');
    amendments.forEach((amendmentEl) => {
      addDiff(amendmentEl, amendmentsWrapperEl.dataset.segmentContent)
    });
  }

  function addDiff(amendmentEl, segmentText) {
    const diffEl = buildMarkup(segmentText, amendmentEl.innerText);
    amendmentEl.innerHTML = ''; // eslint-disable-line no-param-reassign
    amendmentEl.appendChild(diffEl);
  }

  return { updateDiff, loadDiff, addDiff };
}

export default amendmentDiffModule;
