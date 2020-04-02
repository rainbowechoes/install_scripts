import requests
import re
import os


class MavenImport(object):
    def __init__(self):
        self.work_dir = 'F:\\jar'
        self.install_command = 'mvn install:install-file -DartifactId={0} -Dversion={1} -DgroupId={2} -Dpackaging=jar -Dfile={3}'
        self.repository_api = 'https://mvnrepository.com/search?q='

    # 返回工作目录下的所有jar文件名
    def __file_yield(self):
        for file in os.listdir(self.work_dir):
            items = file.split(".")
            file_extension = items[len(items) - 1]
            if file_extension == "jar":
                yield file 

    # 远程方式获取groupId
    def __maven_jar_group(self, artifact_name):
        html_text = requests.get(self.repository_api + artifact_name).text
        href_text = re.findall('class="im-subtitle">(.*?) » ', html_text)[0]
        group_id = re.findall('>(.*?)<', href_text)[0]
        return group_id

    # 本地方式获取groupId
    def __local_jar_group(self, artifact_name):
        return str(artifact_name).replace("-", ".")

    # 抽取参数，将参数放在列表中返回
    def __extract_param(self, file_full_name):
        file_short_name = str(os.path.splitext(file_full_name)[0])
        # 从全文件名中摘取artifactId和version
        position = file_short_name.rfind("-")
        artifact_id = file_short_name[:position]
        version = file_short_name[position + 1:]
        return [artifact_id, version]

    # 扫描目录，从maven远程仓库爬取groupId导入jar包
    def import_from_repository(self):
        os.chdir(self.work_dir)
        for file_full_name in self.__file_yield():
            print(file_full_name + "正在导入")
            params = self.__extract_param(file_full_name)

            # 从maven远程仓库爬取groupId
            group_id = self.__maven_jar_group(params[0])

            # maven命令参数，用于格式化maven命令字符串
            params.append(group_id)
            params.append(file_full_name)
            command = self.install_command.format(*params)

            # 执行maven命令
            execute_result = os.popen(command)
            result_str = str(execute_result.read())

            # 通过正则获取提示信息，查看是否导入成功
            if len(re.findall("BUILD SUCCESS", result_str)) > 0:
                print(file_full_name + ": SUCCESS, artifactId: {0}, version: {1}, groupId：{2}, file: {3}".format(*params))
                print('***********************************************')
            else:
                print(file_full_name + ": Fail, Command:" + command)
                print('***********************************************')

    # 扫描目录，本地导入jar包，直接将groupId设置为artifactId
    def import_from_local(self):
        os.chdir(self.work_dir)
        for file_full_name in self.__file_yield():
            print(file_full_name + "正在导入")
            params = self.__extract_param(file_full_name)

            # 直接将artifactId设置为groupId
            group_id = self.__local_jar_group(params[0])

            # maven命令参数，用于格式化maven命令字符串
            params.append(group_id)
            params.append(file_full_name)
            command = self.install_command.format(*params)

            # 执行maven命令
            execute_result = os.popen(command)
            result_str = str(execute_result.read())

            # 通过正则获取提示信息，查看是否导入成功
            if len(re.findall("BUILD SUCCESS", result_str)) > 0:
                print(file_full_name + ": SUCCESS, artifactId: {0}, version: {1}, groupId：{2}, file: {3}".format(*params))
                print('***********************************************')
            else:
                print(file_full_name + ": Fail, Command:" + command)
                print('***********************************************')


if __name__ == '__main__':
    importUtil = MavenImport()
    choice = input("选择导入方式(1为本地导入，0为远程导入):")
    if choice == "1":
        importUtil.import_from_local()
    else:
        importUtil.import_from_repository()