
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
  constructor(outerDiv, contentDiv, formDiv, button) {
    this.outerDiv = outerDiv;
    this.contentDiv = contentDiv;
    this.formDiv = formDiv;
    this.button = button;

    this.addEventListeners();
  }

  addEventListeners() {
    this.button.addEventListener('click', this.toggleEditable.bind(this));
    this.button.addEventListener('focus', this.handleButtonFocus.bind(this));
    document.addEventListener('keydown', this.handleKeyDown.bind(this));
    document.addEventListener('click', this.handleDocumentClick.bind(this));
  }

  toggleEditable() {
    const isEditable = this.contentDiv.getAttribute('contenteditable') === 'true';
    if (isEditable) {
      this.contentDiv.setAttribute('contenteditable', 'false');
      // change the value of a hidden input field
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
    if (isEditable) {
      this.outerDiv.classList.remove('bg-sub-alt-color');
      this.outerDiv.classList.add('bg-sub-color');
      this.contentDiv.classList.remove('text-sub-color', 'hover:text-text-color', 'focus:text-text-color');
      this.contentDiv.classList.add('text-main-color', 'focus:text-text-color');
      this.formDiv.classList.remove('opacity-0', 'group-hover:opacity-100');
      this.button.classList.add('text-text-color', 'focus:text-main-color');
    } else {
      this.outerDiv.classList.remove('bg-sub-color');
      this.outerDiv.classList.add('bg-sub-alt-color');
      this.contentDiv.classList.remove('text-main-color', 'focus:text-text-color');
      this.contentDiv.classList.add('text-sub-color', 'hover:text-text-color', 'focus:text-text-color');
      this.formDiv.classList.add('opacity-0', 'group-hover:opacity-100');
      this.button.classList.remove('text-text-color', 'focus:text-main-color');
      this.button.classList.add('text-sub-color', 'hover:text-text-color', 'focus:text-text-color');
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

  handleButtonFocus(event) {
    const isEditable = this.contentDiv.getAttribute('contenteditable') === 'true';
    const isTabKey = event.key === 'Tab';
    if (isEditable && !isTabKey) {
      this.outerDiv.classList.remove('bg-sub-color');
      this.outerDiv.classList.add('bg-sub-alt-color');
      this.contentDiv.addEventListener('focus', this.handleContentDivFocus.bind(this));
    } else {
      this.outerDiv.classList.remove('bg-sub-alt-color');
      this.outerDiv.classList.add('bg-sub-color');
    }
  }

  handleContentDivFocus() {
    const isEditable = this.contentDiv.getAttribute('contenteditable') === 'true';
    if (isEditable) {
      this.outerDiv.classList.remove('bg-sub-alt-color');
      this.outerDiv.classList.add('bg-sub-color');
      this.contentDiv.addEventListener('focus', this.handleContentDivFocus.bind(this));
    } else {
      this.outerDiv.classList.remove('bg-sub-alt-color');
      this.outerDiv.classList.add('bg-sub-color');
    }

  }

  // reloads if Esc pressed in contenteditable mode
  handleKeyDown(event) {
    const isEditable = this.contentDiv.getAttribute('contenteditable') === 'true';
    if (isEditable && event.key === 'Escape' || event.key === 'Esc') {
      event.preventDefault();
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


export function handleKeydownEvent(element, isCtrl=false, isShift=false, isAlt=false, key) {
  $(document).keydown(function(event) {
    if (
      (!isCtrl || (event.ctrlKey || event.metaKey)) &&
      (!isShift || event.shiftKey) &&
      (!isAlt || event.altKey) &&
      event.key === key
    ) {
      event.preventDefault();
      element.focus();
    }
  });
}