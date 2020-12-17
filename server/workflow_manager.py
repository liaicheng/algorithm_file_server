from file_manager import FileManager
import redis
from util import date
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)


data_root = "/Users/lac/PycharmProjects/algorithm_file_server/data/"
users = ["u001"]
class WorkflowManager():
    def __init__(self,redis,user=""):
        self.redis = redis
        self.file_manager = FileManager(redis)
        self.user = user

    #每日定时，按批生成待处理文件
    def begin_batch_process(self):
        dt = date.get_date_str()
        for i in users:
            self.file_manager.set_owner(i)
            self.file_manager.generate_file(data_root+i)
            self.redis.set(i+"_"+dt,"preprocess")
            self.redis.expire(i+"_"+dt, 3600)

    def on_process(self,name):
        dt = date.get_date_str()
        rv = self.redis.get(name+"_"+dt)
        res = ""
        print(rv)
        if rv and rv == b"preprocess":
            self.file_manager.set_file_name(name+".xls")
            self.redis.set(name + "_" + dt, "processing")
            # fb = self.file_manager.download_and_process_file()
            fb="/data/"+name+".xls"
            res = fb
        return res

    def on_finish(self,name):
        dt = date.get_date_str()
        rv = self.redis.get(name + "_" + dt)
        res = None
        if rv and rv == b"processing":
            self.redis.set(name + "_" + dt, "finished")
        return res


if __name__ == "__main__":
    wm = WorkflowManager(r,"")
    wm.begin_batch_process()
    # wm.on_process("u001")
    #
    # wm.on_finish("u001")