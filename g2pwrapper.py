import tempfile
import subprocess
import os

PYTHON_VERSION = 'python2.7'
PATH_G2P = os.path.expanduser('~/g2p/')


def createTmpFile(suffix, prefix, path):
    tmp = tempfile.mkstemp(suffix, prefix, dir=path, text=True)

    return tmp


class G2PWrapper:

    def __init__(self, model, path):
        self.model = model  # trained g2p model to use
        self.path = os.path.expanduser(path)

    def transcribeWord(self, word):

        # create temporary file, as g2p wants its input to reside inside a file
        file_id, fname = createTmpFile('.txt', 'tmp_g2pwrapper', None)

        # file is not yet fully opened
        file = open(file_id, mode='w')

        # print(file, fname)

        # write the word to the file
        file.write(word.upper())
        # make sure it's been written
        file.flush()

        # close the file to enable the subprocess to open it on its end
        file.close()

        # run g2p as a subprocess under python2 which will ouput its result on stdout, captured by CompletedProcess cp
        cp = subprocess.run(
            ['%s' % PYTHON_VERSION, '%sg2p.py' % self.path, '--model', 'data/%s' % self.model, '--apply',
             '%s' % fname], stdout=subprocess.PIPE)

        # now we may remove the temporary file
        os.remove(fname)

        # return value is in byte format -> decode using utf8
        result = cp.stdout.decode('UTF-8')
        # retrieve pronunciation only
        result = result.split()[1:]
        # fuse pronunciation back together
        result = ' '.join(result)

        return result


if __name__ == '__main__':
    wrapper = G2PWrapper('model-6', PATH_G2P)
    print(wrapper.transcribeWord('horse'))
