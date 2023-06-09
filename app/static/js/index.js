
import { UtilsBarColorTransition, UtilsItemColorTransition, Timer, handleCopyContent, handleFlashMessage, handleKeydownEvent, createUtilsItem, createChatbotServerMessage, handleUtilsItemUpdate, handleUtilsItemDelete, handleChatbotServerMessageUpdate, handleChatbotUserMessageUpdate, handleChatbotUserMessageDelete } from './utils.js';


// prevent running jQuery code before finish loading document
$(document).ready(function() {
  // todolist search query
  $("#todolist-search-form").submit(function(event) {
    event.preventDefault();
    $("#todolist-list .utils-item").fadeOut(300);   // hide all items before execution
    const todolistItemSearchQuery = $("#todolist-search-input").val().toLowerCase().trim();
    if (todolistItemSearchQuery !== "") {
      $("#todolist-list .utils-item-content").each(function() {
        if ($(this).text().toLowerCase().includes(todolistItemSearchQuery)) {
          $(this).closest("#todolist-list .utils-item").fadeIn(300);   // show items if content matches search query
        }
      });
    } else {
      $("#todolist-list .utils-item").fadeIn(300);   // show all items if seaarch query is empty
    }
  });

  // control color transition of search bars
  const TodolistBarInput = new UtilsBarColorTransition($("#todolist-input-outerDiv"), $("#todolist-input-input"), $("#todolist-input-button"));
  const TodolistBarSearch = new UtilsBarColorTransition($("#todolist-search-outerDiv"), $("#todolist-search-input"), $("#todolist-search-button"));
  const ChatbotBarInput = new UtilsBarColorTransition($("#chatbot-input-outerDiv"), $("#chatbot-input-input"), $("#chatbot-input-button"));
  
  // retain scroll progress of chatbot between refreshes
  $("#todolist-list").scrollTop(localStorage.getItem("todolistScrollPosition"));
  $("#todolist-list").scroll(function() {
    localStorage.setItem("todolistScrollPosition", $(this).scrollTop());
  });
  
  // retain scroll progress of todolist between refreshes
  $("#chatbot-message-container").scrollTop(localStorage.getItem("chatbotScrollPosition"));
  $("#chatbot-message-container").scroll(function() {
    localStorage.setItem("chatbotScrollPosition", $(this).scrollTop());
  });

  // copy content of certain class to clipboard when clicked
  $(".utils-item-content").each(function() {
    handleCopyContent($(this));
  });
  
  // prevent default enter key behavior in specified elements (todolist bars)
  $("input").each(function() {
    $(this).keypress(function(event) {
      if (event.key === "Enter") {
        event.preventDefault();
      }
    });
  });

  // focus certain elements on certain keyboard events
  handleKeydownEvent($("#todolist-input-input"), "focus", true, true, false, "P");
  handleKeydownEvent($("#todolist-search-input"), "focus", false, true, true, "F");

  // handle user data upload
  $("#user-data-upload-button").click(function() {
    $("#user-data-upload-input").click();
  });
  $("#user-data-upload-form").on("change", function() {
    if ($("#user-data-upload-input:file").length === 1) {
      $("#user-data-upload-form").submit();
    }
  });

  // control color transition of items on "edit" toggle
  $(".utils-item:not(.no-custom-transition").each(function() {
    const TodolistItemTransition = new UtilsItemColorTransition($(this), $(this).find("div.utils-item-content"), $(this).find("button.utils-item-update-button"));
  });

  // handle todolist insertion
  $("#todolist-input-form").submit(function(event) {
    event.preventDefault();
    var todolistApiRouteCreate = "/api/todolist/create";
    fetch(todolistApiRouteCreate, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "todolist-create": $("#todolist-input-input").val(),
      }),
    })
      .then(response => response.json())
      .then(handleFlashMessage)
      .then(data => {
        // clear form input after submission
        
        var utilsItem = createUtilsItem(data["id"], data["value"]);
        $("#todolist-list").append(utilsItem);   // append to parent div as last element
        const utilsItemElem = $("#todolist-list").find(".utils-item:last");

        handleCopyContent(utilsItemElem.find(".utils-item-content"));   // copy content to clipboard
        const utilsItemColorTransition = new UtilsItemColorTransition(utilsItemElem, utilsItemElem.find(".utils-item-content"), utilsItemElem.find("button.utils-item-update-button"));   // handle color transition
        
        // communication with backend
        handleUtilsItemUpdate(utilsItemElem.find("button.utils-item-update-button"), "/api/todolist/update");
        handleUtilsItemDelete(utilsItemElem.find("button.utils-item-delete-button"), "/api/todolist/delete");
        // do something to scroll to bottom
      })
      .catch(error => {
        console.error(error);
      });
  });

  // handle todolist update
  $("#todolist-list button.utils-item-update-button").each(function() {
    handleUtilsItemUpdate($(this), "/api/todolist/update");
  });

  // handle todolist deletion
  $("#todolist-list button.utils-item-delete-button").each(function() {
    handleUtilsItemDelete($(this), "/api/todolist/delete");
  });

  // control timer
  const timer = new Timer($("#timer-button-play"), $("#timer-button-pause"), $("#timer-button-skip"), $("#timer-display-number"), $("#timer-display-progress"), $("#timer-display-container"), $("#timer-display-gif"));

  // handle chatbot server msg creation
  // do something to prevent multiple form submission
  $("#chatbot-input-form").submit(function(event) {
    event.preventDefault();
    var chatbotApiRouteUserMessageCreate = "/api/chatbot/user-msg/create";
    var chatbotApiRouteServerMessageCreate = "/api/chatbot/server-msg/create";
    fetch(chatbotApiRouteUserMessageCreate, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        "chatbot-user-msg-create": $("#chatbot-input-input").val(),
      }),
    })
      .then(response => response.json())
      .then(handleFlashMessage)
      .then(data => {
        var userMessage = createUtilsItem(data["id"], data["value"]);
        $("#chatbot-message-container").append(userMessage);
        const userMessageElem = $("#chatbot-message-container").find(".utils-item:last");

        handleCopyContent(userMessageElem.find(".utils-item-content"));   // copy content to clipboard
        const utilsItemColorTransition = new UtilsItemColorTransition(userMessageElem, userMessageElem.find(".utils-item-content"), userMessageElem.find("button.utils-item-update-button"));   // handle color transition

        // communication with backend
        handleChatbotUserMessageUpdate(userMessageElem.find("button.utils-item-update-button"), "/api/chatbot/user-msg/update");
        handleChatbotUserMessageDelete(userMessageElem.find("button.utils-item-delete-button"), "/api/chatbot/user-msg/delete");

        return fetch(chatbotApiRouteServerMessageCreate, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            "chatbot-server-msg-create": $("#chatbot-input-input").val(),
          }),
        })
          .then(response => response.json())
          .then(handleFlashMessage)
          .then(data => {
            var serverMessage = createChatbotServerMessage(data["id"], data["value"]);
            $("#chatbot-message-container").append(serverMessage);
            const serverMessageElem = $("#chatbot-message-container").find(".utils-item:last");

            handleCopyContent(serverMessageElem.find(".utils-item-content"));   // copy content to clipboard
            handleChatbotServerMessageUpdate(serverMessageElem.find("button.utils-item-update-button-server"), "/api/chatbot/server-msg/update");
          })
          .catch(error => {
            console.error(error);
          });
      })
  })

  // handle chatbot user msg update
  $("#chatbot-message-container button.utils-item-update-button").each(function() {
    handleChatbotUserMessageUpdate($(this), "/api/chatbot/user-msg/update");
  });

  // handle chatbot user msg deletion
  $("#chatbot-message-container button.utils-item-delete-button").each(function() {
    handleChatbotUserMessageDelete($(this), "/api/chatbot/user-msg/delete");
  });

  // handle chatbot server msg update
  $("#chatbot-message-container button.utils-item-update-button-server").each(function() {
    handleChatbotServerMessageUpdate($(this), "/api/chatbot/server-msg/update");
  });
});