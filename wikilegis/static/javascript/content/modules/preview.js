import $ from 'jquery';

function previewModule() {

  function additiveAmendmentPreview(inputEl) {
    const tabWrapperEl = $(inputEl).closest('[data-tab-container]')[0];
    const previewWrapperEl = tabWrapperEl.querySelector('[data-additive-preview]');
    previewWrapperEl.innerText = inputEl.value;
  }

  return { additiveAmendmentPreview }

}

export default previewModule;
