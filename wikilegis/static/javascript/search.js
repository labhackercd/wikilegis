import List from 'list.js';

const options = {
  searchClass: 'banner__search',
  listClass: 'wikilegis__bills-list',
  valueNames: ['item__title', 'item__text'],
};

const billsListSearch = new List('bills-list-search', options);

export default billsListSearch;
