function errorMessage(msg) {
  console.log(msg);
  var div = $('<div>', {"class": 'alert alert-danger alert-dismissable'});
  div.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>');
  div.append($('<strong>').text(msg));
  return $('#todo').before(div);
}

var socket = io();

var app = new Vue({
  el: '#todo',
  delimiters: ['((', '))'],
  data: {
    todos: [],
    newToDo: '',
  },
  methods: {
    addToDo: function() {
      $.ajax('/todos', {
        method: 'POST',
        data: {
          description: this.newToDo,
        },
        success: () => {
          console.log("New Todo " + this.newToDo);
          this.newToDo = "";
          this.getToDos();
        },
        error: (response) => {
          errorMessage(response.responseJSON.message)
        }
      })
    },
    getToDos: function() {
      $.getJSON('/todos', {}, this.updateToDos)
    },
    updateToDos: function(data) {
      this.todos = data.todos;
      console.log('Updated todos');
    },
    toggleDone: function(todo_id) {
      $.ajax("/todos/" + todo_id, {
        method: "PUT",
        success:  () => {
          console.log("Toggled todo " + todo_id);
          this.getToDos();
        },
      })
    },
    deleteToDo: function(todo_id) {
      $.ajax("/todos/" + todo_id, {
        method: "DELETE",
        success:  () => {
          console.log("DELETED todo " + todo_id);
          this.getToDos();
        },
        error: () => {
          errorMessage(response.responseJSON.message)
        }
      })
    }
  }
})

app.getToDos();
socket.on('update', app.getToDos)
