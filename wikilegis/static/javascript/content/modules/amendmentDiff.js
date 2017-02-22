import $ from 'jquery';

const diff = require('diff');

function amendmentDiffModule() {
    function updateDiff(inputEl) {
        const containerEL = $(inputEl).closest('[data-segment-content]')[0]
        const segmentContent = containerEL.dataset.segmentContent;
        const diffEl = buildMarkup(diff.diffWordsWithSpace(segmentContent, inputEl.value));

        const diffWrapperEl = containerEL.querySelector('[data-diff-wrapper]');
        diffWrapperEl.innerHTML = '';
        diffWrapperEl.appendChild(diffEl);
    }

    function buildMarkup(diff) {
        let diffElement = document.createDocumentFragment();
        diff.forEach((part) => {
            let className = '';
            if (part.added) className = 'diff-added';
            else if (part.removed)  className = 'diff-removed';

            let span = document.createElement('span');
            $(span).addClass(className);
            span.appendChild(document.createTextNode(part.value));
            diffElement.appendChild(span);
        })
        return diffElement;
    }

    return { updateDiff };
}

export default amendmentDiffModule;
