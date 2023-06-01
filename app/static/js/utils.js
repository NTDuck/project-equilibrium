
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
  constructor(playButton, pauseButton, skipButton, numberDiv, progressDiv, containerDiv, image) {
    this.playButton = playButton;
    this.pauseButton = pauseButton;
    this.skipButton = skipButton;
    this.numberDiv = numberDiv;
    this.progressDiv = progressDiv;
    this.containerDiv = containerDiv;
    this.image = image;

    this.maxWidth = this.containerDiv.width();
    this.timerInterval = null;

    this.audioApiRoute = "/api/audio-files";
    this.audioFolder = "/static/audio";

    this.imageApiRoute = "/api/timer-image-files";
    this.imageFolder = "/static/images/gifs/timer";

    this.sessionCountApiRoute = "/api/update-timer-session-count";

    this.init();
  }
  
  init() {
    this.addEventListeners();
    this.prepareTimerConfig();
    this.prepareAudio();
    this.prepareDisplayImages();
  }

  // warning: should move fetch() outside event listeners
  addEventListeners() {
    this.playButton.click(this.toggleState.bind(this));
    this.pauseButton.click(this.toggleState.bind(this));
    this.skipButton.click(this.skip.bind(this));
    window.addEventListener("beforeunload", this.saveProgress.bind(this));
    
    // bind spacebar to play/pause buttons
    $(document).keydown((event) => {
      if (event.shiftKey && event.key === " ") {
        event.preventDefault();
        this.toggleState();
      }
    });

    // bind Shift + N to skip button
    $(document).keydown((event) => {
      if (event.shiftKey && event.key === "N") {
        event.preventDefault();
        this.skip();
      }
    });
  }

  // warning: fetch request not fully resolved when called
  prepareTimerConfig() {
    fetch("/api/timer-config")
      .then(response => response.json())
      .then(timerConfigs => {
        this.workSessionLength = timerConfigs["work"] * 60;
        this.shortBreakSessionLength = timerConfigs["short_break"] * 60;
        this.longBreakSessionLength = timerConfigs["long_break"] * 60;
        this.pomodoroInterval = timerConfigs["interval"];
        this.timerCountSpeed = timerConfigs["delay"];
      })
      .then(() => {
        // part of constructor, placed here to prevent fetch request not fully resolved
        this.timerState = "paused";
        this.currentSession = "work";
        this.sessionsCompleted = 0;
        this.timerCount = this.workSessionLength;
        this.timerCountMax = this.timerCount;
      })
      .then(() => {
        this.loadSavedProgress();
      })
      .then(() => {
        this.updateDisplay();
      })
      .catch(error => {
        console.error("Error retrieving timer config values:", error);
      });
  }

  // warning: fetch request not fully resolved when called
  prepareAudio() {
    let audioSessionCompleteFolder = "timer-session-complete";
    let audioStatusChangeFolder = "timer-status-change";
    
    // retrieve all files from designated folders
    fetch(`${this.audioApiRoute}/${audioSessionCompleteFolder}`)
      .then(response => response.json())
      .then(audioFiles => {
        this.audioSessionComplete = audioFiles.map(fileUrl => new Audio(`${this.audioFolder}/${audioSessionCompleteFolder}/${fileUrl}`));
      });

    fetch(`${this.audioApiRoute}/${audioStatusChangeFolder}`)
      .then(response => response.json())
      .then(audioFiles => {
        this.audioStatusChange = audioFiles.map(fileUrl => new Audio(`${this.audioFolder}/${audioStatusChangeFolder}/${fileUrl}`));
      });
  }

  prepareDisplayImages() {
    this.imagePausedFolder = "paused";
    this.imagePlayingWorkFolder = "playing-work";
    this.imagePlayingShortBreakFolder = "playing-short-break";
    this.imagePlayingLongBreakFolder = "playing-long-break";
    
    fetch(`${this.imageApiRoute}/${this.imagePausedFolder}`)
      .then(response => response.json())
      .then(imageFiles => {
        this.imagesPaused = imageFiles;
      });
    fetch(`${this.imageApiRoute}/${this.imagePlayingWorkFolder}`)
      .then(response => response.json())
      .then(imageFiles => {
        this.imagesPlayingWork = imageFiles;
      });
    fetch(`${this.imageApiRoute}/${this.imagePlayingShortBreakFolder}`)
      .then(response => response.json())
      .then(imageFiles => {
        this.imagesPlayingShortBreak = imageFiles;
      });
    fetch(`${this.imageApiRoute}/${this.imagePlayingLongBreakFolder}`)
      .then(response => response.json())
      .then(imageFiles => {
        this.imagesPlayingLongBreak = imageFiles;
      });
  }

  updateSessionCount() {
    fetch(`${this.sessionCountApiRoute}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ "session-count": 1 }),
    })
      .catch(error => {
        console.error(error);
      })
  }

  // play random audio from list
  playAudio(audio) {
    let selectedAudio = Math.floor(Math.random() * audio.length);
    audio[selectedAudio].play();
  }

  getImage(images) {
    let selectedImage = Math.floor(Math.random() * images.length);
    return images[selectedImage];
  }

  loadSavedProgress() {
    const savedProgress = JSON.parse(localStorage.getItem("timerProgress"));
    if (savedProgress) {
      this.timerState = savedProgress.timerState;
      this.currentSession = savedProgress.currentSession;
      this.sessionsCompleted = savedProgress.sessionsCompleted;
      this.timerCount = savedProgress.timerCount;
      this.timerCountMax = savedProgress.timerCountMax;
    }
  }

  saveProgress() {
    const progressData = {
      timerState: "paused",   // make sure always paused when page gets reloaded
      currentSession: this.currentSession,
      sessionsCompleted: this.sessionsCompleted,
      timerCount: this.timerCount,
      timerCountMax: this.timerCountMax,
    };
    localStorage.setItem("timerProgress", JSON.stringify(progressData));
  }

  changeGifSrc() {
    // don't even ask where this crap comes from
    if (this.timerState === "paused") {
      this.image.attr("src", `${this.imageFolder}/${this.imagePausedFolder}/${this.getImage(this.imagesPaused)}`);
    } else {
      if (this.currentSession === "work") {
        this.image.attr("src", `${this.imageFolder}/${this.imagePlayingWorkFolder}/${this.getImage(this.imagesPlayingWork)}`);
      } else if (this.currentSession === "shortBreak") {
        this.image.attr("src", `${this.imageFolder}/${this.imagePlayingShortBreakFolder}/${this.getImage(this.imagesPlayingShortBreak)}`);
      } else {
        this.image.attr("src", `${this.imageFolder}/${this.imagePlayingLongBreakFolder}/${this.getImage(this.imagesPlayingLongBreak)}`);
      }
    }
    // subtle animation
    this.image.hide();
    this.image.fadeIn(300);
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
      if (this.sessionsCompleted >= this.pomodoroInterval) {
        this.currentSession = "longBreak";
        this.timerCount = this.longBreakSessionLength;
        this.sessionsCompleted = 0;
      } else {
        this.currentSession = "shortBreak";
        this.timerCount = this.shortBreakSessionLength;
      }
    } else if (this.currentSession !== "work") {
      this.currentSession = "work";
      this.timerCount = this.workSessionLength;
      this.updateSessionCount();   // only update session count after breaks
    }
    this.timerCountMax = this.timerCount;
    this.timerState = "paused";


    this.updateDisplay();
    this.changeGifSrc();
    this.playAudio(this.audioStatusChange);
    this.playAudio(this.audioSessionComplete);
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

    // update colors
    if (this.timerState === "paused") {
      this.numberDiv.fadeIn(300);
      this.progressDiv.removeClass("bg-text-color bg-main-color").addClass("bg-sub-color");
      this.containerDiv.removeClass("bg-sub-color").addClass("bg-bg-color");
      this.pauseButton.hide();
      this.pauseButton.removeClass("text-sub-color").addClass("text-text-color");
      this.playButton.show();
    } else {
      this.numberDiv.fadeOut(300);
      if (this.currentSession === "work") {
        this.progressDiv.removeClass("bg-sub-color bg-text-color").addClass("bg-main-color");
      } else {
        this.progressDiv.removeClass("bg-sub-color bg-main-color").addClass("bg-text-color");
      }
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
    this.changeGifSrc();
    this.playAudio(this.audioStatusChange);
    this.updateDisplay();
  }
}


export function handleKeydownEvent(element, triggerEvent, isCtrl, isShift, isAlt, key) {
  $(document).keydown(function(event) {
    if (
      (!isCtrl || (event.ctrlKey || event.metaKey)) &&
      (!isShift || event.shiftKey) &&
      (!isAlt || event.altKey) &&
      event.key === key
    ) {
      event.preventDefault();
      element.trigger(triggerEvent);
    }
  });
}