"use strict";

function addToDo() {
  let form = document.getElementById('addToDo')
  let formData = new FormData(form);

  $.ajax("/todos", {
    method: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: (result) => {
      location.reload();
    },
    error: (result) => {
      console.log(result)
    }
  });
  return false;
}

function toggleDone(id) {
  $.ajax("/todos/" + id, {
    method: "PUT",
    success: (result) => {
      console.log("Toggled ToDo " + id);
      location.reload();
    }
  });
}

function deleteToDo(id) {
  $.ajax("/todos/" + id, { 
    method: "DELETE",
    success: (result) => {
      console.log("Deleted ToDo " + id);
      location.reload();
    }
  });
}
