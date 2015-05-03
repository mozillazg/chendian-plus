var MemberInfo = React.createClass({
  loadDataFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  getInitialState: function() {
    return {data: {}};
  },

  componentDidMount: function() {
    this.loadDataFromServer();
  },

  render: function() {
    var member = this.state.data;
    member.nick_name = member.nick_name || 'nick_name';
    member.description = member.description || 'description';
    var url = '/m/' + member.id;
    var memberInfo = (
      <div className="member">
        <div className="avatar-120 col-md-5">
          <a href={url}>
            <img data-src="holder.js/120x120/random" className="img-rounded"
              alt={member.nick_name} style={{width: "120px", height: "120px"}}
              src={member.avatar} title={member.nick_name} id="member-avatar" />
          </a>
        </div>
        <div className="detail col-md-7">
          <ul className="list-unstyled">
            <li>编号: <span>{member.sn}</span></li>
            <li>昵称: <span className="editable" data-name="nick_name"
                        data-value={member.nick_name} data-type="text"
                      >{member.nick_name}</span></li>
          </ul>
        </div>
      </div>
      );
    return (
      <div className="member-info">
        {memberInfo}
        <div className="description col-md-12">
          <div className="editable" data-name="description"
           data-value={member.description} data-type="textarea">{member.description}</div>
        </div>
      </div>
    );
  }
});

var Book = React.createClass({
  render: function() {
    var book = this.props.book;
    var url = '/b/' + book.id + '/';
    return (
      <li className="book" data-author="" data-desc={book.description}>
        <a href={url}>
          <img data-src="holder.js/200x288" className="img-rounded"
            alt={book.name} src={book.cover} title={book.name}/>
          <span className="well well-sm">{book.name}</span>
        </a>
      </li>
    );
  }
});

var BookList = React.createClass({
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    var bookNodes = this.state.data.map(function (book) {
      return (
        <Book book={book} key={book.id}>
        </Book>
      )
    });
    return (
      <ul className="list-inline book-list">
        {bookNodes}
      </ul>
    );
  }
});


var memberID = $('#profile').data('id');
var memberURL = '/api/members/' + memberID + '/';
var initEditable = function() {
  $('.member-info .editable').editable({
    url: memberURL,
    pk: memberID,
    autotext: 'always',
    validate: function(value) {
      if($.trim(value) == '') {
        return 'This field is required';
      }
    }
  });
};
React.render(
  <MemberInfo url={memberURL} />,
  document.getElementById('profile'),
  function() {
    if ($("#profile").data('editable')) {
      initEditable();
    }
  }
);

var checkinsURL = memberURL + 'checkins/';
React.render(
  <CheckinList url={checkinsURL} per_page="30" />,
  document.getElementById('checkin-list')
);


var booksURL = memberURL + 'books/';
React.render(
  <BookList url={booksURL} />,
  document.getElementById('read-books')
);
