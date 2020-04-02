from qiniu import Auth, put_file
import os

class QiniuUpload:
    # 1. modify ak and sk as yours
    __access_key = "KU8PRQ2zNFSul7Whm0423ktQYskFm96GXcbYlUvL"
    __secret_key = "0C7l4Ec5eGmEDVlW0VrKR9FzzSzflLgQUG1qNenk"

    def __init__(self, bucket_name, bucket_url, save_file, word_dir):
        self.__bucket_name = bucket_name
        self.__bucket_url = bucket_url
        self.__save_file = save_file
        self.__work_dir = word_dir
        self.__upload_request = Auth(self.__access_key, self.__secret_key)

    # get all image files in work dir
    def get_files(self):
        os.chdir(self.__work_dir)
        for file in os.listdir(self.__work_dir):
            items = file.split(".")
            extension = items[len(items) - 1]
            image_file_extension = ("png", "jpg", "jpeg")
            if extension in image_file_extension:
                yield file

    # call the qiniuyun's API interface to upload file 
    def upload_image(self, image_file_name, image_file_path):
        token = self.__upload_request.upload_token(self.__bucket_name, image_file_name, 3600)
        put_file(token, image_file_name, image_file_path)
        print("\t图片上传成功")

        # if you want to remove file after upload, you can enable the below code 
        # os.remove(image_file_name)
        # print("-------------------")
        # print("\t图片删除成功")

    # generate a image file's md_link according the bucket_url and filename
    def generate_image_link(self, image_file_name):
        link_url = 'http://%s/%s' % (self.__bucket_url, image_file_name)

        image_name = image_file_name.split(".")
        md_url = '![%s](%s)\n' % (image_name[0], link_url)
        print("\t外链生成成功")
        return md_url

    # save one file md url into txt file 
    def save_to_txt(self, image_md_url):
        with open(self.__save_file, "a", encoding="utf-8") as f:
            f.write(image_md_url)
        print("\t外链保存至文本")

    # save the newest image's md url into clipboard
    def save_to_clip_board(self, image_md_url):
        command = 'echo ' + image_md_url.strip() + '| clip'
        os.system(command)
        print("\t外链保存至剪贴板")


if __name__ == '__main__':
    # 2. modify the four configs as yours
    bucket_name = "markdown"
    bucket_url = "image.rainbowecho.top"
    save_file = "image_md_path.txt"
    work_dir = "F:\\md image\\"

    upload = QiniuUpload(bucket_name, bucket_url, save_file, work_dir)
    print("-------------------")
    print("找到文件: ")
    for file_full_name in upload.get_files():
        print(file_full_name)
        path = "./" + file_full_name
        upload.upload_image(file_full_name, path)
        url_before_save = upload.generate_image_link(file_full_name)
        upload.save_to_clip_board(url_before_save)
        upload.save_to_txt(url_before_save)
