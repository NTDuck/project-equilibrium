
import { TodolistComponent } from './utils/todolist.js';
import { EnterKeyPrevention } from './utils/EnterKeyPrevention.js';


// instantiate
const TodolistComponentInput = new TodolistComponent('todolist-input-outerDiv', 'todolist-input-input', 'todolist-input-button');
const TodolistComponentSearch = new TodolistComponent('todolist-search-outerDiv', 'todolist-search-input', 'todolist-search-button');

const TodolistInputInputEnterKeyPrevention = new EnterKeyPrevention('todolist-input-input');
const TodolistSearchInputSearchKeyPrevention = new EnterKeyPrevention('todolist-search-input');


// define copy-to-clipboard feature

// get all todolistItemCopyButtons
const todolistItemCopyButtons = document.querySelectorAll('.todolist-item-copyButton');

// iterate over each todolistItemCopyButton and attach event listener
todolistItemCopyButtons.forEach(todolistItemCopyButton => {
  todolistItemCopyButton.addEventListener('click', () => {

    // DOM traversal, refer to app/templates/macros.html
    const todolistItemContent = todolistItemCopyButton.closest('.todolist-item').querySelector('.todolist-item-content');
    
    // copy the content of todolistItemContent to clipboard
    navigator.clipboard.writeText(todolistItemContent.textContent)
      .catch((error) => {
        console.error("Clipboard API error: ", error)
      });
  })
})


// define search feature

const todolistItemSearchInput = document.getElementById('todolist-search-input');
const todolistItemSearchButton = document.getElementById('todolist-search-button');
const todolistItemContents = document.getElementById('todolist-list').querySelectorAll('.todolist-item-content');

// attach event listener
todolistItemSearchButton.addEventListener('click', () => {

  // make sure all todolistItems are re-displayed between queries
  const todolistItems = document.querySelectorAll('.todolist-item');
  todolistItems.forEach(todolistItem => {
    todolistItem.style.removeProperty('display');
  });

  // get the search query
  const todolistItemSearchQuery = todolistItemSearchInput.value.trim().toLowerCase();

  // iterate over content of each todolistItem and hide/show based on search query
  if (todolistItemSearchQuery !== '') {
    for (let i = 0; i < todolistItemContents.length; i++) {
      const todolistItemContentText = todolistItemContents[i].textContent.toLowerCase();
      if (!todolistItemContentText.includes(todolistItemSearchQuery)) {
        todolistItemContents[i].closest('.todolist-item').style.display = 'none';
  }}}
})