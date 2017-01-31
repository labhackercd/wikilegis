import { paths } from '../config';

function addMultiplePaths(...args) {
  const newPath = args.join('/');

  paths.update(newPath);
  window.history.pushState(null, null, newPath);
}

function addPath(name, id) {
  if (window.location.pathname.indexOf(name) === -1) {
    const path = window.location.pathname;
    const newPath = path === '/' ? `/${name}/${id}` : `${path}/${name}/${id}`;

    paths.update(newPath);
    window.history.pushState(null, null, newPath);
  }
}

function removePath(name) {
  const path = window.location.pathname;
  const nameIndex = path.indexOf(`/${name}`);
  const newPath = path.slice(0, nameIndex) === '' ? '/' : path.slice(0, nameIndex);

  paths.update(newPath);
  window.history.pushState(null, null, newPath);
}

function updatePath(newPath) {
  window.history.replaceState(null, null, newPath);
}

function updateHash(newPath, hash) {
  if (hash !== paths.hash) {
    paths.update(undefined, hash);
    window.history.pushState(null, null, newPath);
  }
}

export {
  addMultiplePaths,
  addPath,
  removePath,
  updatePath,
  updateHash,
};
