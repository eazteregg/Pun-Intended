import tempfile
import subprocess
import os

def createTmpFile(suffix, prefix, path):

    tmp = tempfile.mkstemp(suffix, prefix, dir=path, text=True)

    return tmp


class G2PWrapper:

    def __init__(self, model, path):

        self.model = model
        self.path = os.path.expanduser(path)


    def transcribeWord(self, word):

        file_id, fname = createTmpFile('.txt', 'tmp_g2pwrapper', None)

        file = open(file_id, mode='w')

        print(file, fname)

        file.write(word.upper())

        file.close()

        cp = subprocess.run(['%sg2p.py' % self.path, '--model', '%s%s' % (self.path, self.model), '--apply', '%s' % fname], stdout=subprocess.PIPE)

        os.remove(fname)

        result = cp.stdout.decode('UTF-8')
        result = result.split()[1:]
        result = ' '.join(result)


        return result


if __name__ == '__main__':

    wrapper = G2PWrapper('model-6', '~/g2p/')
    print(wrapper.transcribeWord('horse'))
