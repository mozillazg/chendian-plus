var Note = React.createClass({displayName: "Note",
  render: function() {
    var note = this.props.note;
    return (
      React.createElement("div", {className: "checkin"}, 
        React.createElement("div", {className: "checkin-author"}, 
          React.createElement("a", {href: note.author_url}, note.author_name), 
          React.createElement("span", {className: "time"}, note.created_at)
        ), 
        React.createElement("div", {className: "checkin-content"}, 
          this.props.children
        )
      )
    );
  }
});

var Notes = React.createClass({displayName: "Notes",
  mixins: [PaginationMixin],

  render: function() {
    if (this.state.loading) {
      return this.loading();
    } else if (this.state.total_count == 0) {
      $('.book-detail').addClass('col-md-5').removeClass('col-md-4');
      $('.checkin-list').addClass('col-md-7').removeClass('col-md-4');
      $('.hundred-goal-note-list').hide();
      return false;
    }

    var noteNodes = this.state.data.map(function (note) {
      var think = newline2br(filterXSS(note.note));
      var bookURL = '/b/name/' + note.book_name + '/';
      var key = "note-" + note.id;
      return (
        React.createElement(Note, {note: note, key: key}, 
          React.createElement("span", {dangerouslySetInnerHTML: {__html: think}})
        )
      )
    });
    return (
      React.createElement("div", null, 
        noteNodes, 
        React.createElement("nav", null, 
          React.createElement("ul", {className: "pager"}, 
            React.createElement("li", {className: "previous"}, React.createElement("a", {href: "javascript: void(0);", onClick: this.handlePerPageClick}, 
                React.createElement("span", {"aria-hidden": "true"}, "←"), " Previous")), 
            React.createElement("li", null, React.createElement("span", {className: "text-center"}, "第 ", this.state.page, " / ", this.state.max_page, " 页")), 
            React.createElement("li", {className: "next"}, React.createElement("a", {href: "javascript: void(0);", onClick: this.handleNextPageClick}, 
                "Next ", React.createElement("span", {"aria-hidden": "true"}, "→")))
          )
        )
      )
    );
  }
});
