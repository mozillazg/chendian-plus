var memberID = $('#profile').data('id');
var memberURL = '/api/members/' + memberID + '/';

var MemberInfo = React.createClass({
  loadDataFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      beforeSend: function() {
        this.setState({loading: true});
        return true;
      }.bind(this),
      success: function(data) {
        this.setState({data: data, loading: false});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  getInitialState: function() {
    return {data: {}};
  },
  loading: function() {
    return (
      <div dangerouslySetInnerHTML={{__html: loadingDiv()}} />
    )
  },

  componentDidMount: function() {
    this.loadDataFromServer();
  },

  render: function() {
    if (this.state.loading) {
      return this.loading();
    }

    var member = this.state.data;
    member.nick_name = member.nick_name || 'nick_name';
    member.description = member.description || 'description';
    var url = '/m/' + member.id + '/';
    var memberInfo = (
      <div className="member">
        <div className="avatar-120 col-md-5 avatar">
          <a href={url} title={member.nick_name}>
            <img className="img-rounded"
              alt={member.nick_name} style={{width: "120px", height: "120px"}}
              src={member.avatar} id="member-avatar" />
          </a>
        </div>
        <div className="detail col-md-7">
          <ul className="list-unstyled">
            <li>编号: <span>{member.sn}</span></li>
            <li>昵称: <span id="member-nick-name">{member.nick_name}</span></li>
          </ul>
        </div>
      </div>
      );
    return (
      <div className="member-info">
        {memberInfo}
        <div className="description col-md-12">
          <div id="member-description">{member.description}</div>
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
        <a href={url} title={book.name}>
          <img className="img-rounded"
            alt={book.name} src={book.cover}/>
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
      beforeSend: function() {
        this.setState({loading: true});
        return true;
      }.bind(this),
      success: function(data, status, xhr) {
        this.setState({data: data, loading: false});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  loading: function() {
    return (
      <div dangerouslySetInnerHTML={{__html: loadingDiv()}} />
    )
  },
  render: function() {
    if (this.state.loading) {
      return this.loading();
    }
    if (this.state.count) {
      $("#read_count").text("（" + this.state.count + " 本）");
    }
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

ReactDOM.render(
  <MemberInfo url={memberURL} />,
  document.getElementById('profile')
);

var checkinsURL = memberURL + 'checkins/';
var perPage = isMobile.any ? 3 : 5;
ReactDOM.render(
  <CheckinList url={checkinsURL} per_page={perPage} />,
  document.getElementById('checkin-list')
);


var booksURL = memberURL + 'books/?_fields=id,name,cover';
ReactDOM.render(
  <BookList url={booksURL} />,
  document.getElementById('read-books')
);
