
import { UtilsBarColorTransition, UtilsItemColorTransition, Timer, handleCopyContent, handleKeydownEvent, createUtilsItem, handleUtilsItemUpdate, handleUtilsItemDeletion } from './utils.js';


// prevent running jQuery code before finish loading document
$(document).ready(function() {
  // search query
  $("#todolist-search-button").click(function() {
    $(".utils-item").fadeOut(300);
    const todolistItemSearchQuery = $("#todolist-search-input").val().toLowerCase().trim();
    if (todolistItemSearchQuery !== '') {
      $(".utils-item-content").each(function() {
        if ($(this).text().toLowerCase().includes(todolistItemSearchQuery)) {
          $(this).closest('.utils-item').fadeIn(300);
        }
      });
    }
  });

  // copy content of certain class to clipboard when clicked
  $(".item-copy-content").each(function() {
    handleCopyContent($(this));
  });
  
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

  // prevent default enter key behavior in specified elements (todolist bars)
  $(".preventEnterKey").each(function() {
    $(this).keypress(function(event) {
      if (event.key === "Enter") {
        event.preventDefault();
      }
    });
  });

  // focus certain elements on certain keyboard events
  handleKeydownEvent($("#todolist-input-input"), "focus", true, true, false, "P");
  handleKeydownEvent($("#todolist-search-input"), "focus", false, true, true, "F");

  // control color transition of search bars
  const TodolistBarInput = new UtilsBarColorTransition($("#todolist-input-outerDiv"), $("#todolist-input-input"), $("#todolist-input-button"));
  const TodolistBarSearch = new UtilsBarColorTransition($("#todolist-search-outerDiv"), $("#todolist-search-input"), $("#todolist-search-button"));
  const ChatbotBarInput = new UtilsBarColorTransition($("#chatbot-input-outerDiv"), $("#chatbot-input-input"), $("#chatbot-input-button"));
  
  // control color transition of items on "edit" toggle
  $(".utils-item").each(function() {
    const TodolistItemTransition = new UtilsItemColorTransition($(this), $(this).find("div.utils-item-content"), $(this).find("form.utils-item-edit-form"), $(this).find("button.utils-item-edit-button"));
  });

  // control timer
  const timer = new Timer($("#timer-button-play"), $("#timer-button-pause"), $("#timer-button-skip"), $("#timer-display-number"), $("#timer-display-progress"), $("#timer-display-container"), $("#timer-display-gif"));

  // handle user data upload
  $("#user-data-upload-button").click(function() {
    $("#user-data-upload-input").click();
  });
  $("#user-data-upload-form").on("change", function() {
    if ($("#user-data-upload-input:file").length === 1) {
      $("#user-data-upload-form").submit();
    }
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
        "todolist-item-add": $("#todolist-input-input").val(),
      }),
    })
      .then(response => response.json())
      .then(todolistInsertValue => {
        var utilsItem = createUtilsItem(todolistInsertValue, "/api/todolist/update", "/api/todolist/delete", "todolist-item-edit", "todolist-item-delete", "todolist-item-edit-form", "todolist-item-delete-form");
        $("#todolist-list").append(utilsItem);   // append to parent div as last element
        const utilsItemElem = $("#todolist-list").find("div.utils-item:last");

        handleCopyContent(utilsItemElem.find("div.utils-item-content"));   // copy content to clipboard
        const TodolistItemTransition = new UtilsItemColorTransition(utilsItemElem, utilsItemElem.find("div.utils-item-content"), utilsItemElem.find("form.utils-item-edit-form"), utilsItemElem.find("button.utils-item-edit-button"));   // handle color transition
        
        // communication with backend
        handleUtilsItemUpdate(utilsItemElem.find("form.todolist-item-edit-form"), "/api/todolist/update");
        handleUtilsItemDeletion(utilsItemElem.find("form.todolist-item-delete-form"), "/api/todolist/delete");
        // do something to scroll to bottom
      })
      .catch(error => {
        console.error(error);
      })
  });

  // handle todolist update
  $("form.todolist-item-edit-form").each(function() {
    handleUtilsItemUpdate($(this), "/api/todolist/update");
  });

  // handle todolist deletion
  $("form.todolist-item-delete-form").each(function() {
    handleUtilsItemDeletion($(this), "/api/todolist/delete");
  });
});