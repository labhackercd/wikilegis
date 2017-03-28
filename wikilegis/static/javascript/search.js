import List from 'list.js';

const options = {
  searchClass: 'banner__search',
  listClass: 'wikilegis__bill-list',
  valueNames: ['item__title', 'item__description'],
};

const billsListSearch = new List('bill-list-search', options);
console.log(billsListSearch)

export default billsListSearch;
