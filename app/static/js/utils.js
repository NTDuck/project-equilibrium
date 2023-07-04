
export class UtilsBarColorTransition {
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


export class UtilsItemColorTransition {
  constructor(outerDiv, contentDiv, button) {
    this.outerDiv = $(outerDiv);
    this.contentDiv = $(contentDiv);
    this.button = $(button);

    this.addEventListeners();
  }

  addEventListeners() {
    this.button.on("click", this.toggleEditable.bind(this));
    this.button.on("focus", this.handleButtonFocus.bind(this));
    $(document).on("keydown", this.handleKeyDown.bind(this));
    $(document).on("click", this.handleDocumentClick.bind(this));
  }

  toggleEditable() {
    const isEditable = this.contentDiv.attr("contenteditable") === "true";
    if (isEditable) {
      this.contentDiv.attr("contenteditable", "false");
      this.button.attr("type", "submit");
      this.button.blur();
    } else {
      this.contentDiv.attr("contenteditable", "true");
      this.button.attr("type", "button");
      this.contentDiv.focus();
      this.setCaretToEnd(this.contentDiv[0]);
    }
    this.updateStyles(!isEditable);
  }

  updateStyles(isEditable) {
    // if (isEditable) {
    //   this.outerDiv.removeClass("bg-sub-alt-color").addClass("bg-sub-color");
    //   this.contentDiv.removeClass("text-sub-color hover:text-text-color focus:text-text-color").addClass("text-main-color focus:text-text-color");
    //   this.button.addClass("text-text-color focus:text-main-color").removeClass("text-sub-color hover:text-text-color focus:text-text-color");
    // } else {
    //   this.outerDiv.removeClass("bg-sub-color").addClass("bg-sub-alt-color");
    //   this.contentDiv.removeClass("text-main-color focus:text-text-color").addClass("text-sub-color hover:text-text-color focus:text-text-color");
    //   this.button.removeClass("text-text-color focus:text-main-color").addClass("text-sub-color hover:text-text-color focus:text-text-color");
    // }
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
    const isEditable = this.contentDiv.attr("contenteditable") === "true";
    const isTabKey = event.key === "Tab";
    if (isEditable && !isTabKey) {
      // this.outerDiv.removeClass("bg-sub-color").addClass("bg-sub-alt-color");
      this.contentDiv.on("focus", this.handleContentDivFocus.bind(this));
    } else {
      // this.outerDiv.removeClass("bg-sub-alt-color").addClass("bg-sub-color");
    }
  }

  handleContentDivFocus() {
    const isEditable = this.contentDiv.attr("contenteditable") === "true";
    if (isEditable) {
      // this.outerDiv.removeClass("bg-sub-alt-color").addClass("bg-sub-color");
      this.contentDiv.on("focus", this.handleContentDivFocus.bind(this));
    } else {
      // this.outerDiv.removeClass("bg-sub-alt-color").addClass("bg-sub-color");
    }
  }

  // reloads if Esc pressed in contenteditable mode
  handleKeyDown(event) {
    const isEditable = this.contentDiv.attr("contenteditable") === "true";
    if (isEditable && (event.key === "Escape" || event.key === "Esc")) {
      event.preventDefault();
      location.reload();
    }
  }

  // reloads if clicked outside item in contenteditable mode
  handleDocumentClick(event) {
    const isEditable = this.contentDiv.attr("contenteditable") === "true";
    const target = event.target;

    if (isEditable && !this.outerDiv.is(target) && !this.outerDiv.has(target).length) {
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

    this.imageApiRoute = "/api/timer/image-files";
    this.imageFolder = "/static/images/gifs/timer";

    this.sessionCountApiRoute = "/api/timer/session-count/update";

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
      if ((event.ctrlKey || event.metaKey) && event.key === " ") {
        event.preventDefault();
        this.toggleState();
      }
    });

    // bind Shift + N to skip button
    $(document).keydown((event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === "N") {
        event.preventDefault();
        this.skip();
      }
    });
  }

  // warning: fetch request not fully resolved when called
  prepareTimerConfig() {
    fetch("/api/timer/config")
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
      body: JSON.stringify({
        "session-count": 1,
      }),
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
    var currentWidthPercentage = ((this.timerCountMax - this.timerCount) / this.timerCountMax) * 100;
    this.progressDiv.css("width", currentWidthPercentage + "%");    

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


export function handleCopyContent(element) {
  element.click(function() {
    navigator.clipboard
      .writeText(element.text())
      .catch(function(error) {
        console.error(error);
      })
  });
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


export function createUtilsItem(id, value) {
  // should be identical to utilsItem in macros.html
  var htmlString = `
  <div id="utils-item-${id}" class="flex flex-row items-center py-2 px-4 max-w-full h-fit bg-sub-alt-color rounded-lg group snap-start transition-colors duration-300 utils-item">
    <div class="flex-grow line-clamp-[99] transition-all duration-300 text-sub-color hover:text-text-color focus:text-text-color cursor-pointer caret-caret-color text-sm utils-item-content">${value}</div>
    <div class="flex flex-col flex-none justify-between pb-[1%] text-sub-color opacity-0 group-hover:opacity-100 transition-all duration-500">
      <button type="button" class="transition-colors duration-300 fill-current text-sub-color hover:text-text-color focus:text-text-color utils-item-update-button">
        <svg class="fill-inherit inline-block w-4 h-4 ml-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
          <path d="M441 58.9L453.1 71c9.4 9.4 9.4 24.6 0 33.9L424 134.1 377.9 88 407 58.9c9.4-9.4 24.6-9.4 33.9 0zM209.8 256.2L344 121.9 390.1 168 255.8 302.2c-2.9 2.9-6.5 5-10.4 6.1l-58.5 16.7 16.7-58.5c1.1-3.9 3.2-7.5 6.1-10.4zM373.1 25L175.8 222.2c-8.7 8.7-15 19.4-18.3 31.1l-28.6 100c-2.4 8.4-.1 17.4 6.1 23.6s15.2 8.5 23.6 6.1l100-28.6c11.8-3.4 22.5-9.7 31.1-18.3L487 138.9c28.1-28.1 28.1-73.7 0-101.8L474.9 25C446.8-3.1 401.2-3.1 373.1 25zM88 64C39.4 64 0 103.4 0 152V424c0 48.6 39.4 88 88 88H360c48.6 0 88-39.4 88-88V312c0-13.3-10.7-24-24-24s-24 10.7-24 24V424c0 22.1-17.9 40-40 40H88c-22.1 0-40-17.9-40-40V152c0-22.1 17.9-40 40-40H200c13.3 0 24-10.7 24-24s-10.7-24-24-24H88z"/>
          </svg>
        </button>
      <button type="submit" class="transition-colors duration-300 fill-current text-sub-color hover:text-text-color focus:text-text-color utils-item-delete-button">
        <svg class="fill-inherit inline-block w-4 h-4 ml-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512">
          <path d="M170.5 51.6L151.5 80h145l-19-28.4c-1.5-2.2-4-3.6-6.7-3.6H177.1c-2.7 0-5.2 1.3-6.7 3.6zm147-26.6L354.2 80H368h48 8c13.3 0 24 10.7 24 24s-10.7 24-24 24h-8V432c0 44.2-35.8 80-80 80H112c-44.2 0-80-35.8-80-80V128H24c-13.3 0-24-10.7-24-24S10.7 80 24 80h8H80 93.8l36.7-55.1C140.9 9.4 158.4 0 177.1 0h93.7c18.7 0 36.2 9.4 46.6 24.9zM80 128V432c0 17.7 14.3 32 32 32H336c17.7 0 32-14.3 32-32V128H80zm80 64V400c0 8.8-7.2 16-16 16s-16-7.2-16-16V192c0-8.8 7.2-16 16-16s16 7.2 16 16zm80 0V400c0 8.8-7.2 16-16 16s-16-7.2-16-16V192c0-8.8 7.2-16 16-16s16 7.2 16 16zm80 0V400c0 8.8-7.2 16-16 16s-16-7.2-16-16V192c0-8.8 7.2-16 16-16s16 7.2 16 16z"/>
        </svg>
      </button>
    </div>
  </div>
  `;
  return htmlString;
}


export function createChatbotServerMessage(id, value) {
  // should be identical to chatbotServerMsg in macros.html
  var htmlString = `
  <div id="utils-item-${id}" class="flex flex-row items-center py-2 px-4 max-w-full h-fit bg-sub-alt-color rounded-lg group snap-start transition-colors duration-300 utils-item no-custom-transition">
  <div class="flex-grow line-clamp-[99] transition-all duration-300 text-sub-color hover:text-text-color focus:text-text-color cursor-pointer caret-caret-color text-sm utils-item-content">${value}</div>
  <div class="flex flex-col flex-none justify-between pb-[1%] text-sub-color opacity-0 group-hover:opacity-100 transition-all duration-500">
    <button type="submit" class="transition-colors duration-300 fill-current text-sub-color hover:text-text-color focus:text-text-color utils-item-update-button-server">
      <svg class="fill-inherit inline-block w-4 h-4 ml-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
        <path d="M142.9 142.9c62.2-62.2 162.7-62.5 225.3-1L327 183c-6.9 6.9-8.9 17.2-5.2 26.2s12.5 14.8 22.2 14.8H463.5c0 0 0 0 0 0H472c13.3 0 24-10.7 24-24V72c0-9.7-5.8-18.5-14.8-22.2s-19.3-1.7-26.2 5.2L413.4 96.6c-87.6-86.5-228.7-86.2-315.8 1C73.2 122 55.6 150.7 44.8 181.4c-5.9 16.7 2.9 34.9 19.5 40.8s34.9-2.9 40.8-19.5c7.7-21.8 20.2-42.3 37.8-59.8zM16 312v7.6 .7V440c0 9.7 5.8 18.5 14.8 22.2s19.3 1.7 26.2-5.2l41.6-41.6c87.6 86.5 228.7 86.2 315.8-1c24.4-24.4 42.1-53.1 52.9-83.7c5.9-16.7-2.9-34.9-19.5-40.8s-34.9 2.9-40.8 19.5c-7.7 21.8-20.2 42.3-37.8 59.8c-62.2 62.2-162.7 62.5-225.3 1L185 329c6.9-6.9 8.9-17.2 5.2-26.2s-12.5-14.8-22.2-14.8H48.4h-.7H40c-13.3 0-24 10.7-24 24z"/>
      </svg>
    </button>
  </div>
</div>
  `;
  return htmlString;
}


export function handleUtilsItemUpdate(button, apiRoute) {
  button.on("click", function(event) {
    if ($(this).attr("type") === "button") {
      return;
    }
    event.preventDefault();
    fetch(apiRoute, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "id": $(this).closest(".utils-item").attr("id").split("-")[2],
        "todolist-update": $(this).closest(".utils-item").find(".utils-item-content").text(),
      }),
    })
      .catch(error => {
        console.error(error);
      })
  });
}


export function handleUtilsItemDelete(button, apiRoute) {
  button.on("click", function(event) {
    event.preventDefault();
    fetch(apiRoute, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "id": $(this).closest(".utils-item").attr("id").split("-")[2],
      }),
    })
      .then($(this).closest(".utils-item").remove())
      .catch(error => {
        console.error(error);
      });
  });
}


export function handleChatbotUserMessageUpdate(button, apiRoute) {
  button.on("click", function(event) {
    if ($(this).attr("type") === "button") {
      return;
    }
    event.preventDefault();
    var userMessageElem = $(this).closest(".utils-item");
    var serverMessageElem = userMessageElem.next(".utils-item");
    fetch(`${apiRoute}/user`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "id": userMessageElem.attr("id").split("-")[2],
        "chatbot-user-msg-update": userMessageElem.find(".utils-item-content").text(),
      }),
    })
      .then(response => response.json())
      .then(() => {
        serverMessageElem.hide();
        serverMessageElem.nextAll().remove();

        return fetch(`${apiRoute}/server`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            "id": serverMessageElem.attr("id").split("-")[2],
            "chatbot-user-msg-last": userMessageElem.find(".utils-item-content").text(),
          }),
        })
          .then(response => response.json())
          .then(data => {
            serverMessageElem.find(".utils-item-content").text(data["value"]);
            serverMessageElem.show();
          });
      })
      .catch(error => {
        console.error(error);
      });
  });
}


export function handleChatbotUserMessageDelete(button, apiRoute) {
  button.on("click", function(event) {
    event.preventDefault();
    var userMessageElem = $(this).closest(".utils-item");
    fetch(apiRoute, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "id": userMessageElem.attr("id").split("-")[2],
      }),
    })
      .then(() => {
        userMessageElem.nextAll().remove();
        userMessageElem.remove();
      })
      .catch(error => {
        console.error(error);
      });
  });
}


export function handleChatbotServerMessageUpdate(button, apiRoute) {
  button.on("click", function(event) {
    event.preventDefault();
    var serverMessageElem = $(this).closest(".utils-item");
    var userMessageElem = serverMessageElem.prev(".utils-item");
    serverMessageElem.hide();
    serverMessageElem.nextAll().remove();
    fetch(apiRoute, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "id": serverMessageElem.attr("id").split("-")[2],
        "chatbot-user-msg-last": userMessageElem.find(".utils-item-content").text(),
      }),
    })
      .then(response => response.json())
      .then(data => {
          serverMessageElem.find(".utils-item-content").text(data["value"]);
          serverMessageElem.show();
        })
      .catch(error => {
        console.error(error);
      })
  });
}