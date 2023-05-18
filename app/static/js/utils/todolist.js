
export class TodolistComponent {
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