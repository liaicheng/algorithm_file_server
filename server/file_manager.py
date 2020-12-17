import pandas as pd
import json
import numpy as np

DATA_ROOT = "/Users/lac/PycharmProjects/algorithm_file_server/data/"

class FileManager(object):
    def __init__(self,redis):
        self.owner = ""
        self.status = ""
        self.file_name = ""
        self.redis_cli = redis

    def set_owner(self,owner):
        self.owner = owner

    def set_status(self,status):
        self.status = status

    def set_file_name(self,name):
        self.file_name = name

    #生成文件数据
    def generate_file(self,path):
        self.generate_single_excel(path)
        self.file_name = ""
        self.status = "preprocess"

    #下载文件
    def download_and_process_file(self):
        with open(self.file_name,"wb") as f:
            file_bytes =f.readlines()

        self.set_status("processing")
        return file_bytes

    def process(self):
        pass

    def generate_single_excel(self,path):
        with open(path) as f:
            data_tmp = json.load(f)
        keys = list(data_tmp[0].keys())

        res = [keys]
        for i in data_tmp:
            tmp = [v for k,v in i.items()]
            res.append(tmp)

        df = pd.DataFrame(res)
        df.to_excel(DATA_ROOT+self.owner+".xls",index=False)


if __name__ == "__main__":
    fm = FileManager()