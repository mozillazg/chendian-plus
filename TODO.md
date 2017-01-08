
* [x] 上传图片增加 上传中... 提示
* [x] 修复 更新书籍信息 后没有更新页面上的 ISBN 的值
* [x] ajax 加载内容时增加 loading.... 提示
* [x] 修复 投稿插入图片功能失效的问题
* [x] 从豆瓣抓取图书信息
* [x] fix 搜索功能失效, 搜索结果页面不要包含 #p123
* [x] 限制划过显示图书信息中图书简介的字数
* [x] loading 图片
* [x] react loading
* [x] 修复文章列表页面 ajax 请求出现了重定向
* [x] api 支持 `_exclude`, `_fields` 参数
* [x] 书籍列表页面 API 请求增加 `_fields/_exclude` 参数
* [x] 调整成员列表页面头像大小（加大）
* [x] gulp sass
* [x] 优化书籍列表页面响应时间
* [x] 优化打卡记录列表页面响应时间
* [x] 继续优化书籍列表页面
  * [x] 默认只获取 name, cover
  * [x] 鼠标划过时再获取详情
* [x] 将书籍详情里的 \\n 由之前的 br 改为 p 标签
* [x] 书籍列表图片 lazyloading
* [x] 优化文章列表和文章页面响应
* [x] 使用 django-cache-machine

* 单页应用

* 改为使用 token 认证

* 移动端 APP

* [ ] 年度统计
  * [x] 书
    * [x] 所有书各自被多少人读过
      * [x] models
      * [x] 统计程序
      * [x] api
        * [x] top 20
        * [x] detail
        * [x] export
  * [x] 人
    * [x] 读过的书
      * [x] models
      * [x] 统计程序
      * [x] api
        * [x] list
        * [x] export
    * [x] 读过多少本
      * [x] models
      * [x] 统计程序
      * [x] api
        * [x] get
        * [ ] 读书最多的人 top 20
  * [ ] 前端
    * [ ] 2016
      * [ ] top 20 book
      * [ ] top 20 reader
   * [ ] 我的 2016
     * [ ] 读过的书
     * [ ] export
