function hoverModule() {
  const segmentAddEL = document.getElementsByClassName('segment-add')[0];

  function showSegmentAdd(targetEl) {
    const segmentEl = targetEl.offsetParent;
    segmentEl.appendChild(segmentAddEL);
    segmentAddEL.classList.add('visible');
  }

  function hideSegmentAdd() {
    segmentAddEL.classList.remove('visible');
  }

  return { showSegmentAdd, hideSegmentAdd };
}

export default hoverModule;
