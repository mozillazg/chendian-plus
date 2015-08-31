var Member = React.createClass({
  render: function() {
    var member = this.props.member;
    var url = '/m/' + member.id + '/';
    return (
      <li className="member" data-author="" data-desc={member.note}>
        <a href={url}>
          <img className="img-rounded avatar-64"
            alt={member.nick_name}
            src={member.avatar} title={member.nick_name}/>
        </a>
      </li>
    );
  }
});

var MemberList = React.createClass({
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
      success: function(data) {
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

    var memberNodes = this.state.data.map(function (member) {
      return (
        <Member member={member} key={member.id}></Member>
      )
    });
    return (
      <div ref="list">
        <ul className="list-inline member-list">{memberNodes}</ul>
      </div>
    );
  }
});

React.render(
  <MemberList url='/api/members/?per_page=1000' />,
  document.getElementById('member-list')
);
