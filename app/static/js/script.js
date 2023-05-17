
class TodolistComponent {
  constructor(outerDivId, inputId, buttonId) {
    this.outerDiv = document.getElementById(outerDivId);
    this.input = document.getElementById(inputId);
    this.button = document.getElementById(buttonId);

    this.addEventListeners();
  }

  addEventListeners() {
    this.input.addEventListener('input', this.handleInput.bind(this));
    this.button.addEventListener('focus', this.handleButtonFocus.bind(this));
    this.button.addEventListener('blur', this.handleButtonBlur.bind(this));
  }

  handleInput() {
    if (this.input.value.trim().length > 0) {
      this.outerDiv.classList.remove('bg-sub-alt-color');
      this.outerDiv.classList.add('bg-sub-color');
    } else {
      this.outerDiv.classList.remove('bg-sub-color');
      this.outerDiv.classList.add('bg-sub-alt-color');
    }
  }

  handleButtonFocus() {
    this.outerDiv.classList.remove('bg-sub-color');
    this.outerDiv.classList.add('bg-sub-alt-color');

    if (this.input.value.trim().length > 0) {
      this.input.classList.remove('text-text-color');
      this.input.classList.add('text-main-color');

      this.button.classList.remove('text-sub-color', 'text-text-color');
      this.button.classList.add('text-main-color');
    } else {
      this.input.classList.remove('text-main-color');
      this.input.classList.add('text-text-color');

      this.button.classList.remove('text-sub-color', 'text-main-color');
      this.button.classList.add('text-text-color');
    }
  }

  handleButtonBlur() {
    this.input.classList.remove('text-main-color');
    this.input.classList.add('text-text-color');

    this.outerDiv.classList.remove('bg-sub-alt-color');
    this.outerDiv.classList.add('bg-sub-color');

    this.button.classList.remove('text-text-color', 'text-main-color');
    this.button.classList.add('text-sub-color');
  }
}


// instantiate
const TodolistComponentInput = new TodolistComponent('todolist-input-outerDiv', 'todolist-input-input', 'todolist-input-button');
const TodolistComponentSearch = new TodolistComponent('todolist-search-outerDiv', 'todolist-search-input', 'todolist-search-button');



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
  for (let i = 0; i < todolistItemContents.length; i++) {
    const todolistItemContentText = todolistItemContents[i].textContent.toLowerCase();
    if (!todolistItemContentText.includes(todolistItemSearchQuery)) {
      todolistItemContents[i].closest('.todolist-item').style.display = 'none';
    }
  }
})