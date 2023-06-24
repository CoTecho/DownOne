# DownOne

Manage Special Download Content with Pyimgui

使用Pyimgui重写，顺便学习一下Pyimgui的使用。

Develop with SteamDeck(Windows 11).

## TODO

*为优先制作

- [x] 实现基础的pyimgui框架
- [x] 迁移原来的DownOne功能（基础的 拖拽文件->获取文件信息->勾选文件并开始下载）
- [ ] *读取下载库，把上述DownOne功能用下载库的方式实现，拖拽文件仅用于初始化下载记录
- [ ] 整理下载库
- [ ] 修复没有缓存的下载记录
- [x] *思考页面间通信
    * 模拟一块内存，用于存储页面间共享的数据
    * 用户输入被页面存入内存，再由页面发出内存刷新信号
    * 相关页面收到通知后从内存拿数据刷新自己的显示
- [ ] 封装一些常用的imgui组合控件
- [ ] *与手机文件进行交互
    * 使用标签删除文件
- [x] *获取标签信息
- [x] *本地标签功能
- [ ] 导出标签
- [ ] 根据标签清理下载库
- [ ] 为音乐文件添加信息
- [ ] 管理音乐文件比特率

## 架构

TODO: 不应该用信号槽，应该模拟一块所有窗口共享的内存，每次刷新如果数据改变各窗口也改变

## Sample Explaination

`[SAMPLE.COM]`: WebSite

`[SAMPLE.KEY]`: ID

## Config Explaination

``
