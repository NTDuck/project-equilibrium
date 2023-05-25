
export class TodolistBarColorTransition {
  constructor(outerDiv, input, button) {
    this.outerDiv = outerDiv;
    this.input = input;
    this.button = button;

    this.addEventListeners();
  }

  addEventListeners() {
    $(this.input).on("input", this.handleInput.bind(this));
    $(this.button).on("focus", this.handleButtonFocus.bind(this));
    $(this.button).on("blur", this.handleButtonBlur.bind(this));
  }

  handleInput() {
    if ($(this.input).val().trim().length > 0) {
      $(this.outerDiv).removeClass("bg-sub-alt-color").addClass("bg-sub-color");
    } else {
      $(this.outerDiv).removeClass("bg-sub-color").addClass("bg-sub-alt-color");
    }
  }

  handleButtonFocus() {
    $(this.outerDiv).removeClass("bg-sub-color").addClass("bg-sub-alt-color");

    if ($(this.input).val().trim().length > 0) {
      $(this.input).removeClass("text-text-color").addClass("text-main-color");
      $(this.button).removeClass("text-sub-color text-text-color").addClass("text-main-color");
    } else {
      $(this.input).removeClass("text-main-color").addClass("text-text-color");
      $(this.button).removeClass("text-sub-color text-main-color").addClass("text-text-color");
    }
  }
  
  handleButtonBlur() {
    $(this.input).removeClass("text-main-color").addClass("text-text-color");
    $(this.outerDiv).removeClass("bg-sub-alt-color").addClass("bg-sub-color");
    $(this.button).removeClass("text-text-color text-main-color").addClass("text-sub-color");
  }
}


// using jQuery will yield unexpetected behaviors
export class TodolistItemColorTransition {
  constructor(outerDiv, contentDiv, form, button) {
    this.outerDiv = outerDiv;
    this.contentDiv = contentDiv;
    this.form = form;
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
      this.form.classList.remove('opacity-0', 'group-hover:opacity-100');
      this.button.classList.add('text-text-color', 'focus:text-main-color');
    } else {
      this.outerDiv.classList.remove('bg-sub-color');
      this.outerDiv.classList.add('bg-sub-alt-color');
      this.contentDiv.classList.remove('text-main-color', 'focus:text-text-color');
      this.contentDiv.classList.add('text-sub-color', 'hover:text-text-color', 'focus:text-text-color');
      this.form.classList.add('opacity-0', 'group-hover:opacity-100');
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


export class Timer {
  constructor(playButton, pauseButton, skipButton, numberDiv, progressDiv, containerDiv, workSessionLength, shortBreakSessionLength, longBreakSessionLength, PomodoroInterval, timerCountSpeed) {
    this.playButton = playButton;
    this.pauseButton = pauseButton;
    this.skipButton = skipButton;
    this.numberDiv = numberDiv;
    this.progressDiv = progressDiv;
    this.containerDiv = containerDiv;

    this.workSessionLength = workSessionLength * 60;
    this.shortBreakSessionLength = shortBreakSessionLength * 60;
    this.longBreakSessionLength = longBreakSessionLength * 60;
    this.PomodoroInterval = PomodoroInterval;
    this.timerCountSpeed = timerCountSpeed;   // milliseconds

    this.maxWidth = this.containerDiv.width();
    this.timerInterval = null;
    this.timerState = "paused";
    this.currentSession = "work";
    this.sessionsCompleted = 0;
    this.timerCount = this.workSessionLength;  // Initial timer count set to work session duration
    this.timerCountMax = this.timerCount;

    this.addEventListeners();
    this.initialDisplaySetup();
  }

  addEventListeners() {
    this.playButton.click(this.toggleState.bind(this));
    this.pauseButton.click(this.toggleState.bind(this));
    this.skipButton.click(this.skip.bind(this));
  }

  initialDisplaySetup() {
    this.updateDisplay();
  }

  start() {
    this.timerInterval = setInterval(() => {
      this.updateDisplay();
      if (this.timerCount === 0) {
        this.stop();
        this.sessionComplete();
      } else {
        this.timerCount--;
      }
    }, this.timerCountSpeed);
  }

  stop() {
    clearInterval(this.timerInterval);
  }

  skip() {
    this.stop();
    this.sessionComplete();
  }

  sessionComplete() {
    if (this.currentSession === "work") {
      this.sessionsCompleted++;
      if (this.sessionsCompleted >= this.PomodoroInterval) {
        this.sessionsCompleted = 0;
        this.currentSession = "longBreak";
        this.timerCount = this.longBreakSessionLength;
      } else {
        this.currentSession = "shortBreak";
        this.timerCount = this.shortBreakSessionLength;
      }
    } else if (this.currentSession === "shortBreak" || this.currentSession === "longBreak") {
      this.currentSession = "work";
      this.timerCount = this.workSessionLength;
    }
    this.timerCountMax = this.timerCount;
    this.timerState = "paused";
    this.updateDisplay();
  }

  updateDisplay() {
    function formatTime(seconds) {
      let rawMinutes = Math.floor(seconds / 60);
      let rawSeconds = seconds % 60;
      let formattedMinutes = String(rawMinutes).padStart(2, "0");
      let formattedSeconds = String(rawSeconds).padStart(2, "0");
      return [formattedMinutes, formattedSeconds];
    }

    // update progressDiv width
    var currentWidth = ((this.timerCountMax - this.timerCount) / this.timerCountMax) * this.maxWidth;
    this.progressDiv.width(currentWidth);

    // update numberDiv time
    let [minutes, seconds] = formatTime(this.timerCount);
    this.numberDiv.text(`${minutes}:${seconds}`);

    // update element colors
    if (this.timerState === "paused") {
      this.numberDiv.fadeIn(300);
      this.progressDiv.removeClass("bg-text-color").addClass("bg-sub-color");
      this.containerDiv.removeClass("bg-sub-color").addClass("bg-bg-color");
      this.pauseButton.hide();
      this.playButton.show();
    } else {
      this.numberDiv.fadeOut(300);
      this.progressDiv.removeClass("bg-sub-color").addClass("bg-text-color");
      this.containerDiv.removeClass("bg-bg-color").addClass("bg-sub-color");
      this.playButton.hide();
      this.pauseButton.show();
    }
  }

  toggleState() {
    if (this.timerState === "paused") {
      this.timerState = "playing";
      this.start();
    } else {
      this.timerState = "paused";
      this.stop();
    }
    this.updateDisplay();
  }
}



export function handleKeydownEvent(element, isCtrl, isShift, isAlt, key) {
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