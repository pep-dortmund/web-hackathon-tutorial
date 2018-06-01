"use strict";

var app = new Vue({
  el: '#todo',
  delimiters: ['((', '))'],
  data: {
    todos: [],
    newToDo: {description: null, due_date: null, due_time: null}
  },
  methods: {
    getToDos: function() {
      $.getJSON('/todos', {}, (data) => {
        this.todos = data['todos'];
        console.log("Got Todos");
      });
    },
    toggleDone: function(id) {
      $.ajax("/todos/" + id, {
        method: "PUT",
        success: (result) => {
          console.log("Toggled ToDo " + id);
          this.getToDos();
        }
      });
    },
    deleteToDo: function(id) {
      $.ajax("/todos/" + id, { 
        method: "DELETE",
        success: (result) => {
          console.log("Deleted ToDo " + id);
          this.getToDos();
        }
      });
    },
    addToDo: function() {
      $.ajax("/todos", {
        method: "POST",
        data: this.newToDo,
        success: (result) => {
          this.getToDos();
        },
      });
    }
  },
  computed: {
    allDone: function() {
      if (this.todos.length == 0) {
        return true;
      }

      let n_done = 0;
      this.todos.forEach((todo) => {
        if (todo.done) {
          n_done += 1;
        }
      });
      return n_done == this.todos.length;
    }
  }
})


app.getToDos();
