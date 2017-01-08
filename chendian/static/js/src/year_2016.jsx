var year = $('.year-top').data('year');


var BookRaw = React.createClass({
  render: function() {
    var book = this.props.top_book.book;
    var count = this.props.top_book.reader_count;
    var url = '/b/' + book.id + '/';
    return (
      <tr>
        <td><a href={url} title={book.name}>{book.name}</a></td>
        <td>{count}</td>
      </tr>
    );
  }
});

var BooksTable = React.createClass({
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
    return {data: []};
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
    var BookNodes = this.state.data.map(function (top_book) {
      return (
        <BookRaw top_book={top_book} key={top_book.id}>
        </BookRaw>
      )
    });
    return (
      <table className="table table-striped table-bordered table-hover">
        <thead>
          <tr>
            <th>名称</th>
            <th>读者数（人）</th>
          </tr>
        </thead>
        <tbody>
            {BookNodes}
        </tbody>
      </table>
    );
  }
});

var ReaderRaw = React.createClass({
  render: function() {
    var reader = this.props.reader;
    var url = '/m/' + reader.member.id + '/';
    return (
      <tr>
        <td><a href={url} title={reader.member.nick_name}>{reader.member.nick_name}</a></td>
        <td>{reader.count}</td>
      </tr>
    );
  }
});

var ReadersTable = React.createClass({
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
    return {data: []};
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
    var readerNodes = this.state.data.map(function (reader) {
      return (
        <ReaderRaw reader={reader} key={reader.id}>
        </ReaderRaw>
      )
    });
    return (
      <table className="table table-striped table-bordered table-hover">
        <thead>
          <tr>
            <th>昵称</th>
            <th>数量（本）</th>
          </tr>
        </thead>
        <tbody>
            {readerNodes}
        </tbody>
      </table>
    );
  }
});


var topBookURL = '/api/books/year/' + year + '/top/20/';
ReactDOM.render(
  <BooksTable url={topBookURL} />,
  document.getElementById('year-top-books')
);

var topReaderURL = topBookURL + 'readers/';
ReactDOM.render(
  <ReadersTable url={topReaderURL} />,
  document.getElementById('year-top-readers')
);
