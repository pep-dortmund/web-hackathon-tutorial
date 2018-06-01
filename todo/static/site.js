

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
