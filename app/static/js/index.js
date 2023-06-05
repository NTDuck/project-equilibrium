
import { TodolistBarColorTransition, TodolistItemColorTransition, Timer, handleKeydownEvent } from './utils.js';


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
    $(this).click(function() {
      navigator.clipboard
        .writeText($(this).text())
        .catch(function(error) {
          console.error("Clipboard API error: ", error)
        })
    });
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
  const TodolistBarInput = new TodolistBarColorTransition($("#todolist-input-outerDiv"), $("#todolist-input-input"), $("#todolist-input-button"));
  const TodolistBarSearch = new TodolistBarColorTransition($("#todolist-search-outerDiv"), $("#todolist-search-input"), $("#todolist-search-button"));
  const ChatbotBarInput = new TodolistBarColorTransition($("#chatbot-input-outerDiv"), $("#chatbot-input-input"), $("#chatbot-input-button"));
  
  // control color transition of items on "edit" toggle
  // warning: not yet implemented into jquery, will do in future versions
  const todolistItems = document.querySelectorAll('.utils-item');

  todolistItems.forEach(todolistItem => {
    const todolistItemContent = todolistItem.querySelector('.utils-item-content');
    const todolistItemEditForm = todolistItem.querySelector('.utils-item-edit-form');
    const todolistItemEditButton = todolistItem.querySelector('.utils-item-edit-button');
  
    const TodolistItemTransition = new TodolistItemColorTransition(todolistItem, todolistItemContent, todolistItemEditForm, todolistItemEditButton);
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
});