var Note = React.createClass({
  render: function() {
    var note = this.props.note;
    return (
      <div className="checkin">
        <div className="checkin-author">
          <a href="javascript: void(0)">{note.author_name}</a>
          <span className="time">{note.created_at}</span>
        </div>
        <div className="checkin-content">
          {this.props.children}
        </div>
      </div>
    );
  }
});

var Notes = React.createClass({
  mixins: [PaginationMixin],

  render: function() {
    if (this.state.loading) {
      return this.loading();
    }

    var noteNodes = this.state.data.map(function (note) {
      var think = newline2br(filterXSS(note.note));
      var bookURL = '/b/name/' + note.book_name + '/';
      var key = "note-" + note.id;
      return (
        <Note note={note} key={key}>
          <span dangerouslySetInnerHTML={{__html: think}} />
        </Note>
      )
    });
    return (
      <div>
        {noteNodes}
        <nav>
          <ul className="pager">
            <li className="previous"><a href="javascript: void(0);" onClick={this.handlePerPageClick}>
                <span aria-hidden="true">&larr;</span> Previous</a></li>
            <li><span className="text-center">第 {this.state.page} / {this.state.max_page} 页</span></li>
            <li className="next"><a href="javascript: void(0);" onClick={this.handleNextPageClick}>
                Next <span aria-hidden="true">&rarr;</span></a></li>
          </ul>
        </nav>
      </div>
    );
  }
});