# Scripts

作为一个后端开发人员，总会需要在虚拟机或云主机上进行项目实际测试。这时候往往就会需要安装一些常用的软件，比如Git、Docker、nodejs等等。

一般而言，我们通常只会在系统初次安装后进行这些常用软件的安装。可笔者操作水平有限，有时需要再开一台虚拟机或者是要重置，这时候笔者就很纠结，想着要是有一个安装脚本就好了。

于是，就有了这个项目，为开发环境中常见的软件安装编写了脚本以及提供了其他一些功能性脚本，提升效率。

## 1. 使用

- `.sh`文件用于Linux系统，使用`chmod +x *.sh`命令更改文件执行权限，在执行`./*.sh`即可执行对应的软件安装脚本
- `.bat`文件用于Windows系统，提供常见软件的访问、服务停止及关闭操作。直接双击执行即可。有的脚本需要管理员权限，以管理员权限执行即可。

## 最后

希望觉得不错的小伙伴们多多PR、star。也希望有兴趣的朋友可以为这个项目做一些贡献。
