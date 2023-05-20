
export class TodolistBarColorTransition {
  constructor(outerDiv, input, button) {
    this.outerDiv = outerDiv;
    this.input = input;
    this.button = button;

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


export class TodolistItemColorTransition {
  constructor(outerDiv, contentDiv, button) {
    this.outerDiv = outerDiv;
    this.contentDiv = contentDiv;
    this.button = button;

    this.addEventListeners();
  }

  addEventListeners() {
    this.button.addEventListener('click', this.toggleEditable.bind(this));
    this.contentDiv.addEventListener('keydown', this.handleKeyDown.bind(this));
    document.addEventListener('click', this.handleDocumentClick.bind(this));
  }

  toggleEditable() {
    const isEditable = this.contentDiv.getAttribute('contenteditable') === 'true';
    if (isEditable) {
      this.contentDiv.setAttribute('contenteditable', 'false');
      const inputContent = this.button.closest('.todolist-item-edit-form').querySelector('.todolist-item-edit-content');
      inputContent.value = this.contentDiv.innerText;
      this.button.setAttribute('type', 'submit');
    } else {
      this.contentDiv.setAttribute('contenteditable', 'true');
      this.button.setAttribute('type', 'button');
      this.contentDiv.focus();
      this.setCaretToEnd(this.contentDiv);
    }
    this.updateStyles(!isEditable);
  }

  updateStyles(isEditable) {
    const outerDivClasses = ['bg-sub-alt-color', 'bg-sub-color'];
    const contentDivClasses = ['text-sub-color', 'hover:text-text-color', 'focus:text-text-color', 'text-text-color'];
    const buttonClasses = ['text-sub-color', 'hover:text-text-color', 'focus:text-text-color', 'text-text-color'];
  
    if (isEditable) {
      this.outerDiv.classList.remove(...outerDivClasses);
      this.outerDiv.classList.add('bg-sub-color');
      this.contentDiv.classList.remove(...contentDivClasses);
      this.contentDiv.classList.add('text-text-color');
      this.button.classList.remove(...buttonClasses);
      this.button.classList.add('text-text-color');
    } else {
      this.outerDiv.classList.remove(...outerDivClasses);
      this.outerDiv.classList.add('bg-sub-alt-color');
      this.contentDiv.classList.remove('text-text-color');
      this.contentDiv.classList.add(...contentDivClasses);
      this.button.classList.remove('text-text-color');
      this.button.classList.add(...buttonClasses);
    }
  }  

  setCaretToEnd(element) {
    const range = document.createRange();
    const selection = window.getSelection();
    range.selectNodeContents(element);
    range.collapse(false);
    selection.removeAllRanges();
    selection.addRange(range);
  }

  // reloads if Esc pressed in contenteditable mode
  handleKeyDown(event) {
    const isEditable = this.contentDiv.getAttribute('contenteditable') === 'true';
    const key = event.key;

    if (isEditable && (key === 'Escape' || key === 'Esc')) {
      location.reload();
    }
  }

  // reloads if clicked outside item in contenteditable mode
  handleDocumentClick(event) {
    const isEditable = this.contentDiv.getAttribute('contenteditable') === 'true';
    const target = event.target;

    if (isEditable && !this.outerDiv.contains(target)) {
      location.reload();
    }
  }
}



export function preventDefaultEnterKeyBehavior(element) {
  element.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
      event.preventDefault();
    }
  });
}


export function attachCopyToClipboardListener(element) {
  element.addEventListener('click', () => {
    navigator.clipboard
      .writeText(element.textContent)
      .catch((error) => {
        console.error("Clipboard API error: ", error)
      });
  })
}


export function retainScrollProgress(element) {

  function saveScrollPosition() {
    localStorage.setItem('scrollPosition', element.scrollTop);
  }

  function restoreScrollPosition() {
    const scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition) {
      element.scrollTop = scrollPosition;
    }
  }

  window.addEventListener('beforeunload', saveScrollPosition);
  window.addEventListener('load', restoreScrollPosition);
}