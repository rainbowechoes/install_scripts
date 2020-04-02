import os


# nginx配置中已经添加了https配置，所以运行前需要手动部署证书，将证书文件改名为server.crt和server.key，两个文件放到/opt/nginx_ssl下
class FsInstall(object):
    def __init__(self, home_dir, store_path, tracker='127.0.0.1'):
        self.home_dir = home_dir
        self.store_path = store_path
        self.tracker = tracker

    def install_nginx(self):
        os.system("cd " + self.home_dir)
        os.system("tar -xvf nginx-1.16.1.tar.gz")
        os.system("cd nginx-1.16.1")
        nginx_configure_str = "./configure --prefix=/opt/nginx --sbin-path=/usr/bin/nginx --add-module={}/fastdfs-nginx-module-1.20/src --with-http_stub_status_module --with-http_ssl_module".format(
            self.home_dir)
        os.system(nginx_configure_str)
        os.system("make && make install")
        os.system("cd " + self.home_dir)
        os.system("cp nginx.conf /opt/nginx/conf/nginx.conf -f")
        os.system("nginx")
        os.system("mv nginx /etc/init.d/")
        os.system("chmod 777 /etc/init.d/nginx ")
        os.system("chkconfig --add /etc/init.d/nginx")
        os.system("chkconfig nginx on")
        print("nginx已安装成功并启动")

    def install_ngx_module(self):
        os.system("cd " + self.home_dir)
        os.system("tar -xvf fastdfs-nginx-module-1.20.tar.gz")
        os.system("cd fastdfs-nginx-module-1.20/src/")
        os.system("sed -i 's/\/usr\/local/\/usr/g' config")
        os.system("cp mod_fastdfs.conf /etc/fdfs/")
        os.system(
            "sed -i 's/connect_timeout=2/connect_timeout=10/g' /etc/fdfs/mod_fastdfs.conf")
        configure_str = 's/tracker_server=tracker:22122/tracker_server={}:22122/g'.format(
            self.tracker)
        os.system("sed -i {} /etc/fdfs/mod_fastdfs.conf".format(configure_str))
        os.system(
            "sed -i 's/url_have_group_name = false/url_have_group_name = true/g' /etc/fdfs/mod_fastdfs.conf")
        store_configure_str = 's/store_path0=\/home\/yuqing\/fastdfs/store_path0={}/g'.format(
            self.store_path)
        os.system(
            "sed -i {} /etc/fdfs/mod_fastdfs.conf".format(store_configure_str))
        os.system("cd " + self.home_dir + "/fastdfs-5.12/conf")
        os.system("cp http.conf mime.types /etc/fdfs/")
        print("FastDFS nginx 模块安装成功")

    def __storage_install(self, tracker='127.0.0.1'):
        os.mkdir(self.store_path)
        os.system('cp storage.conf/sample storage.conf')
        os.system(
            "sed -i 's/base_path=\/home\/yuqing\/fastdfs/base_path=\/home\/fastdfs\/storage/g' storage.conf")
        os.system(
            "sed -i 's/store_path0=\/home\/yuqing\/fastdfs/store_path0=\/home\/fastdfs\/storage/g' storage.conf")
        configure_str = 's/tracker_server=192.168.209.121:22122/tracker_server={}:22122/g'.format(
            tracker)
        os.system("sed -i {} storage.conf".format(configure_str))
        os.system("service fdfs_storaged start")
        os.system("chkconfig fdfs_storaged on")

    def __tracker_install(self):
        tracker_base_path = '/home/fastdfs/tracker'
        os.mkdir(tracker_base_path)
        os.system("cp tracker.conf.sample tracker.conf")
        os.system(
            "sed -i 's/base_path=\/home\/yuqing\/fastdfs/base_path=\/home\/fastdfs\/tracker/g' tracker.conf")
        os.system("service fdfs_trackerd start")
        os.system("chkconfig fdfs_trackerd on")
        pass

    def install_fs(self):
        os.system("cd " + self.home_dir)
        os.system("tar -xvf fastdfs-5.12.tar.gz")
        os.system("cd fastdfs-5.12")
        os.system("./make.sh && ./make.sh install")
        # 此时在/etc/fdfs目录下
        os.system("cd /etc/fdfs/")
        self.__tracker_install()
        self.__storage_install(self.tracker)
        print("运行结果：")
        os.system("ps -ef | grep fdfs")
        pass

    def __yum_dependency(self):
        os.system("yum -y install gcc")
        os.system("yum -y install unzip zip")
        os.system("yum -y install libevent")
        os.system(
            "yum -y install pcre pcre-devel zlib zlib-devel openssl openssl-devel")

    def __local_denpendency(self):
        os.system("unzip libfastcommon-1.0.40.zip")
        os.system("cd libfastcommon-1.0.40")
        os.system("./make.sh && ./make.sh install")
        os.system("cd " + self.home_dir)

    def install_dependency(self):
        self.__yum_dependency()
        self.__local_denpendency()


if __name__ == "__main__":
    fsInstall = FsInstall('/root', '/home/fastdfs/storage')
    fsInstall.install_dependency()
    fsInstall.install_fs()
    fsInstall.install_ngx_module()
    fsInstall.install_nginx()
