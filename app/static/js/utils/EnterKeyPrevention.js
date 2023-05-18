
export class EnterKeyPrevention {
  constructor(elementId) {
    this.element = document.getElementById(elementId);
    this.attachEvent();
  }

  attachEvent() {
    this.element.addEventListener('keydown', this.preventEnterSubmission);
  }

  preventEnterSubmission(event) {
    if (event.key === 'Enter') {
      event.preventDefault();
    }
  }
}