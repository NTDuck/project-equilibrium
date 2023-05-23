
import * as utils from './utils/utils.js';


const todolistInputOuterDiv = document.getElementById('todolist-input-outerDiv');
const todolistInputInput = document.getElementById('todolist-input-input');
const todolistInputButton = document.getElementById('todolist-input-button');

const todolistSearchOuterDiv = document.getElementById('todolist-search-outerDiv');
const todolistSearchInput = document.getElementById('todolist-search-input');
const todolistSearchButton = document.getElementById('todolist-search-button');


// simple edit toggle
const todolistItems = document.querySelectorAll('.todolist-item');

todolistItems.forEach(todolistItem => {
  const todolistItemContent = todolistItem.querySelector('.todolist-item-content');
  const todolistItemEditForm = todolistItem.querySelector('.todolist-item-edit-form');
  const todolistItemEditButton = todolistItem.querySelector('.todolist-item-edit-button');

  const TodolistItemTransition = new utils.TodolistItemColorTransition(todolistItem, todolistItemContent, todolistItemEditForm, todolistItemEditButton);
});


// control color transition of search bars
const TodolistBarInput = new utils.TodolistBarColorTransition(todolistInputOuterDiv, todolistInputInput, todolistInputButton);
const TodolistBarSearch = new utils.TodolistBarColorTransition(todolistSearchOuterDiv, todolistSearchInput, todolistSearchButton);


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
  utils.handleKeydownEvent($("#todolist-input-input"), true, true, false, "P");
  utils.handleKeydownEvent($("#todolist-search-input"), false, true, true, "F");
})