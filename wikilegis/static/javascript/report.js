import amendmentDiffModule from './content/modules/amendmentDiff';

const diff = new amendmentDiffModule();

const segmentList = document.querySelectorAll('[data-raw-content]')

segmentList.forEach(segment => {
    const amendmentList = segment.querySelectorAll('[data-modifier-amendment]');
    amendmentList.forEach(amendment => {
        diff.addDiff(amendment, segment.dataset.rawContent);
    })
})