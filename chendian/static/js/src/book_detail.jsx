var BookInfo = React.createClass({
  getInitialState: function() {
    return {data: {}};
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
    var book = this.state.data;
    var bookInfo = (
        <div>
          <h1>{book.name}</h1>
          <div className="bookDescription">
            {book.description}
          </div>
        </div>
      );
    return (
      <div className="bookInfo">
        {bookInfo}
      </div>
    );
  }
});

var Think = React.createClass({
  render: function() {
    return (
      <div className="think">
        <div className="thinkAuthor">
          【{this.props.sn}】{this.props.nickName}({this.props.qq}) {this.props.date}
        </div>
        <div className="thinkContent">
          {this.props.children}
        </div>
      </div>
    );
  }
});

var ThinkList = React.createClass({
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
    var thinkNodes = this.state.data.map(function (think) {
      return (
        <Think sn={think.sn} qq={think.qq} nickName={think.nick_name} date={think.posted_at}>
          {think.think}
        </Think>
      )
    });
    return (
      <div className="panel panel-default">
        <div className="panel-heading">阅读记录</div>
        <div className="panel-body">
          {thinkNodes}
        </div>
        <div className="panel-footer clearfix"></div>
      </div>
    );
  }
});

var bookID = $('#content').data('id');
var bookURL = '/api/books/' + bookID + '/';
React.render(
  <BookInfo url={bookURL} />,
  document.getElementById('content')
);

var thinksURL = bookURL + 'thinks/';
React.render(
  <ThinkList url={thinksURL} />,
  document.getElementById('thinkList')
);
