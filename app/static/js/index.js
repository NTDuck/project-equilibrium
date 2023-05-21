
import * as utils from './utils.js';


const todolistItemList = document.getElementById('todolist-list');
const todolistItemContents = todolistItemList.querySelectorAll('.todolist-item-content');

const todolistInputOuterDiv = document.getElementById('todolist-input-outerDiv');
const todolistInputInput = document.getElementById('todolist-input-input');
const todolistInputButton = document.getElementById('todolist-input-button');

const todolistSearchOuterDiv = document.getElementById('todolist-search-outerDiv');
const todolistSearchInput = document.getElementById('todolist-search-input');
const todolistSearchButton = document.getElementById('todolist-search-button');


// simple search query
todolistSearchButton.addEventListener('click', () => {

  // make sure all items are re-displayed between queries
  const todolistItems = document.querySelectorAll('.todolist-item');
  todolistItems.forEach(todolistItem => {
    todolistItem.style.removeProperty('display');
  });

  // get the search query
  const todolistItemSearchQuery = todolistSearchInput.value.trim().toLowerCase();

  // iterate over content of each item and hide/show based on search query
  if (todolistItemSearchQuery !== '') {
    for (let i = 0; i < todolistItemContents.length; i++) {
      const todolistItemContentText = todolistItemContents[i].textContent.toLowerCase();
      if (!todolistItemContentText.includes(todolistItemSearchQuery)) {
        todolistItemContents[i].closest('.todolist-item').style.display = 'none';
  }}}
})


// simple edit toggle
const todolistItems = document.querySelectorAll('.todolist-item');

todolistItems.forEach(todolistItem => {
  const todolistItemContent = todolistItem.querySelector('.todolist-item-content');
  const todolistItemEditButton = todolistItem.querySelector('.todolist-item-edit-button');

  const TodolistItemTransition = new utils.TodolistItemColorTransition(todolistItem, todolistItemContent, todolistItemEditButton);
});


// control color transition of search bars
const TodolistBarInput = new utils.TodolistBarColorTransition(todolistInputOuterDiv, todolistInputInput, todolistInputButton);
const TodolistBarSearch = new utils.TodolistBarColorTransition(todolistSearchOuterDiv, todolistSearchInput, todolistSearchButton);


// prevent default enter key behavior in certain textinputs; refer to app/templates/macros.html
const preventEnterKeyItems = document.getElementsByClassName('preventEnterKey');
for (const preventEnterKeyItem of preventEnterKeyItems) {
  utils.preventDefaultEnterKeyBehavior(preventEnterKeyItem);
}


// copy item's content to clipboard when clicked
todolistItemContents.forEach(todolistItemContent => {
  utils.attachCopyToClipboardListener(todolistItemContent);
})


// retain scroll progress of todolist between refreshes
utils.retainScrollProgress(todolistItemList);


// focus input bar if Ctrl+Shift+P is pressed
// try this: https://code.visualstudio.com/shortcuts/keyboard-shortcuts-windows.pdf
utils.attachKeyBinding(todolistInputInput, true, true, false, 'P');
utils.attachKeyBinding(todolistSearchInput, true, true, false, 'F');