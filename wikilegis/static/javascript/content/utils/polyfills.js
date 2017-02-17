
function hasClass(el, className) {
  if (el.classList) return el.classList.contains(className);
  return new RegExp(`(^| )${className}( |$)`, 'gi').test(el.className);
}

export { hasClass }; // eslint-disable-line import/prefer-default-export
