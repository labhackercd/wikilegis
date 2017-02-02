function hoverModule() {
  const segmentAddEl = document.getElementsByClassName('segment-add')[0];

  function showSegmentAdd(targetEl) {
    const segmentEl = targetEl.offsetParent;
    segmentEl.appendChild(segmentAddEl);
    segmentAddEl.classList.add('visible');
  }

  function hideSegmentAdd() {
    segmentAddEl.classList.remove('visible');
  }

  return { showSegmentAdd, hideSegmentAdd };
}

export default hoverModule;
