function historyModule() {
  function addMultiple(...args) {
    const url = args.join('/');
    window.history.pushState(null, null, url);
  }

  function add(targetEl, name, id) {
    if (window.location.pathname.indexOf(name) === -1) {
      const path = window.location.pathname;
      const url = path === '/' ? `${name}/${id}/` : `${path}/${name}/${id}/`;
      window.history.pushState(null, null, url);
    }
  }

  function remove(name) {
    const path = window.location.pathname;
    const nameIndex = path.indexOf(`/${name}`);
    const url = path.slice(0, nameIndex) === '' ? '/' : path.slice(0, nameIndex);
    window.history.pushState(null, null, url);
  }

  return { addMultiple, add, remove };
}

export default historyModule;
