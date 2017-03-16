import $ from 'jquery';

function previewModule() {
  function additiveAmendmentPreview(inputEl) {
    const tabWrapperEl = $(inputEl).closest('[data-tab-container]')[0];
    const previewWrapperEl = tabWrapperEl.querySelector('[data-additive-preview]');
    const typeSelectEl = inputEl.previousElementSibling;
    let typeText = typeSelectEl.options[typeSelectEl.selectedIndex].innerText;
    if (!inputEl.value) typeText = '';
    previewWrapperEl.innerHTML = `<strong>${typeText}</strong> ${inputEl.value}`;
  }

  return { additiveAmendmentPreview };
}

export default previewModule;
