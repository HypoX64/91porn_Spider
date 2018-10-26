# 介绍
* 这个是一个使用python构建的获取某网站资源缩略图及视频的简易爬虫

# 基本要求
* 需要能访问得到某不存在的网站(某些校园网因为IPV6或教育网的原因可能可以直接访问)
* 若使用源码运行，需要预先安装python3及第三方包bs4及requests
* 若使用.exe版本运行，请确保PC安装的为Windows的64操作系统，将exe.7z中的文件解压到py源文件所在目录及'./'中后运行即可。

# 使用方法
* 1.修改'./config/config'的配置文件(若只是进行测试，默认配置即可)
* 2.运行download_image获取网站视频缩略图及视频标题，缩略图将保存在'./image'中
* 3.在'./image'查找需要的资源并将缩略图复制到'./choose_video_want_to_download'中
* 4.运行download_video下载视频并生成对应的视频链接文本，值得注意的是由于该网站的限制，同一IP地址每天只能获取10个视频的链接并进行下载

# 配置文件说明
* Model  决定运行模式，view_select_down 将会下载视(由于目前的下载部分代码仍然不完善，不推荐使用这种方法)。view_select_list 将只会生成视频的下载链接脚本文件'./video/videolist.txt'可以将文本复制到迅雷等下载器中进行全速下载至当前文件夹，再运行rename.py将视频文件进行重命名
* VideoType 决定下载的网页部分键值有{all,hot,recently,long,monthdiscuss,monthfavorite,favorite,highlight,monthhot,lastmonthhot}可供选择。什么意思就不用说了吧。。。
* ThreadNum 决定下载的线程数，不易设置过大，防止IP被封。

# 改进
* 改进下载部分代码，实现重连以及多点下载
* 伪造cookie模拟登录，解除一个IP一天只能下10个视频的限制
* 完成友好的GUI界面


