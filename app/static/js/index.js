
import { TodolistBarColorTransition, TodolistItemColorTransition, Timer, handleKeydownEvent } from './utils.js';


// prevent running jQuery code before finish loading document
$(document).ready(function() {
  // search query
  $("#todolist-search-button").click(function() {
    $(".todolist-item").fadeOut(300);
    const todolistItemSearchQuery = $("#todolist-search-input").val().toLowerCase().trim();
    if (todolistItemSearchQuery !== '') {
      $(".todolist-item-content").each(function() {
        if ($(this).text().toLowerCase().includes(todolistItemSearchQuery)) {
          $(this).closest('.todolist-item').fadeIn(300);
        }
      });
    }
  });

  // copy item's content to clipboard when clicked
  $(".todolist-item-content").each(function() {
    $(this).click(function() {
      navigator.clipboard
        .writeText($(this).text())
        .catch(function(error) {
          console.error("Clipboard API error: ", error)
        })
    });
  });

  // retain scroll progress of todolist between refreshes
  $("#todolist-list").scrollTop(localStorage.getItem("todolistScrollPosition"));
  $("#todolist-list").scroll(function() {
    localStorage.setItem("todolistScrollPosition", $(this).scrollTop());
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
  handleKeydownEvent($("#todolist-input-input"), true, true, false, "P");
  handleKeydownEvent($("#todolist-search-input"), false, true, true, "F");

  // control color transition of search bars
  const TodolistBarInput = new TodolistBarColorTransition($("#todolist-input-outerDiv"), $("#todolist-input-input"), $("#todolist-input-button"));
  const TodolistBarSearch = new TodolistBarColorTransition($("#todolist-search-outerDiv"), $("#todolist-search-input"), $("#todolist-search-button"));
  
  // control color transition of items on "edit" toggle
  const todolistItems = document.querySelectorAll('.todolist-item');

  todolistItems.forEach(todolistItem => {
    const todolistItemContent = todolistItem.querySelector('.todolist-item-content');
    const todolistItemEditForm = todolistItem.querySelector('.todolist-item-edit-form');
    const todolistItemEditButton = todolistItem.querySelector('.todolist-item-edit-button');
  
    const TodolistItemTransition = new TodolistItemColorTransition(todolistItem, todolistItemContent, todolistItemEditForm, todolistItemEditButton);
  });

  // control timer
  const timer = new Timer($("#timer-button-play"), $("#timer-button-pause"), $("#timer-button-skip"), $("#timer-display-number"), $("#timer-display-progress"), $("#timer-display-container"), 25, 5, 15, 4, 1000);
  
});