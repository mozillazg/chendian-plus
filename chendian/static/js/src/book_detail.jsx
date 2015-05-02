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
    var url = '/b/' + book.id;
    var bookInfo = (
        <div>
          <div className="cover text-center col-md-6">
            <a href={url}>
              <img data-src="holder.js/160x180/random" className="img-rounded"
                alt={book.name} style={{width: "160px", height: "180px"}}
                src={book.cover} title={book.name}/>
            </a>
          </div>
          <div className="detail col-md-6">
            <ul className="list-unstyled">
              <li>名称：{book.name}</li>
              <li>作者：{book.author}</li>
              <li>ISBN: {book.isbn}</li>
              <li>豆瓣: <a href={book.douban_url} target="_blank">Go to douban</a></li>
            </ul>
          </div>
          <div className="description col-md-12">
            {book.description}
          </div>
        </div>
      );
    return (
      <div className="book-info">
        {bookInfo}
      </div>
    );
  }
});

var Checkin = React.createClass({
  render: function() {
    return (
      <div className="checkin">
        <div className="checkin-author">
          【{this.props.sn}】{this.props.nickName} {this.props.date}
        </div>
        <div className="checkin-content">
          {this.props.children}
        </div>
      </div>
    );
  }
});

var CheckinList = React.createClass({
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
    var checkinNodes = this.state.data.map(function (checkin) {
    var think = checkin.think.replace('\n', '<br />');
      return (
        <Checkin sn={checkin.sn} nickName={checkin.nick_name}
          date={checkin.posted_at}>
          #打卡 《{checkin.book_name}》{think}
        </Checkin>
      )
    });
    return (<div>{checkinNodes}</div>);
  }
});

var bookID = $('#content').data('id');
var bookURL = '/api/books/' + bookID + '/';
React.render(
  <BookInfo url={bookURL} />,
  document.getElementById('content')
);

var checkinsURL = bookURL + 'checkins/';
React.render(
  <CheckinList url={checkinsURL} />,
  document.getElementById('checkin-list')
);
