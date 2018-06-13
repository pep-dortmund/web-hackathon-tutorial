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
    teams: [],
    team: undefined,
    idea: undefined,
    progress: undefined,
    implementation: undefined,
    voted: false,
  },
  methods: {
    getTeams: function() {
      $.getJSON('/teams', {}, this.updateTeams).always(function(data){
        console.log(data)
      });
    },
    updateTeams: function(data) {
      this.teams = data.teams;
      console.log('Updated todos');
    },
    sendVote: function() {
      console.log(this);
      $.post({
        url: '/vote',
        data: {
          team: this.team.name,
          idea: this.idea.name,
          implementation: this.implementation.name,
          progress: this.progress.name,
        },
        success: function(){
          console.log('voted');
          this.voted = true;
        }.bind(this),
        error: function(data){
          console.log(data);
          alert(data.responseJSON.message);
        }
      });
    },
  }
})

app.getTeams();
socket.on('update', app.getTeams)
