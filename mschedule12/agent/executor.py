
import subprocess
import tempfile
from utils import getlogger


logger = getlogger(__name__, 'o:/exec.log')

class Executor:
    def run(self, script:str, timeout=5):
        """
        执行器执行脚本的方法

        :param script: 脚本
        :param timeout: 超时时间
        :return: 返回tuple， (code , text)
        """
        with tempfile.TemporaryFile() as f:
            proc = subprocess.Popen(
                script, shell=True, stdout=f, stderr=f)

            try:
                code = proc.wait(timeout=timeout) # 默认一直等
                f.seek(0)
                if code == 0:
                    txt = f.read()
                else:
                    txt = f.read()


                logger.info('[{} {}]'.format(code, txt))
                return code, txt

            except Exception as e:
                logger.error(e)
                return (1, '')

if __name__ == '__main__':
    exec = Executor()
    ret = exec.run('dir')
    print(ret)


