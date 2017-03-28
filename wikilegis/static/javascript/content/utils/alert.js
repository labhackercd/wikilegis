const alertEl = document.querySelector('[data-wikilegis-alert]');
const headerEl = alertEl.querySelector('[data-alert-header]');
const textEl = alertEl.querySelector('[data-alert-text]');
let timeoutFunction = null;

function dismissAlert() {
  if (timeoutFunction) clearTimeout(timeoutFunction);
  alertEl.classList.add('hidden');
}

function showAlert(errorTitle, errorMessage, alertType = 'error', autoDismiss = true) {
  if (timeoutFunction) {
    clearTimeout(timeoutFunction);
    dismissAlert();
  }

  if (alertType === 'success') {
    alertEl.classList.add('success');
    alertEl.classList.remove('error');
  } else {
    alertEl.classList.remove('success');
    alertEl.classList.add('error');
  }

  headerEl.innerText = errorTitle;
  textEl.innerHTML = errorMessage;
  alertEl.classList.remove('hidden');
  if (autoDismiss) timeoutFunction = setTimeout(dismissAlert, 5000);
}

export {
  showAlert,
  dismissAlert,
};
