''' Unit tests for lpf '''


import unittest2 as unittest
import subprocess

def setUpModule():
    ''' Initiate to a defined set of installed rpms. '''
    with open('/dev/null', 'w') as devnull:
	subprocess.check_call('./remove-lpf-packages', stdout=devnull)
	subprocess.check_call('./make_rpms', stdout=devnull)


class TestLpf(unittest.TestCase):
    ''' Basic tests. '''


    # @unittest.skipIf(not FEDORA, 'Fedora-only test')
    def test_list(self):
        ''' Test lpf list. '''
        with open('/dev/null', 'w') as devnull:
            subprocess.check_call('./test-list', stdout=devnull)

    def test_state(self):
        ''' Test lpf state. '''
        with open('/dev/null', 'w') as devnull:
            subprocess.check_call('./test-state', stdout=devnull)

    def test_approve(self):
        ''' Test lpf approve. '''
        with open('/dev/null', 'w') as devnull:
            subprocess.check_call('./test-approve', stdout=devnull)

    def test_update(self):
        ''' Test lpf update. '''
        with open('/dev/null', 'w') as devnull:
            subprocess.check_call('./test-update', stdout=devnull)

    def test_remove(self):
        ''' Test target package remove. '''
        with open('/dev/null', 'w') as devnull:
            subprocess.check_call('./test-remove', stdout=devnull)

    def test_update_lpf(self):
        ''' Test target lpf package update. '''
        with open('/dev/null', 'w') as devnull:
            subprocess.check_call('./test-update-lpf', stdout=devnull)

    def test_srpm(self):
        ''' Test  srpm and spec command. '''
        with open('/dev/null', 'w') as devnull:
            subprocess.check_call('./test-srpm', stdout=devnull)

    def test_remove_lpf(self):
        ''' Test remove lpf package. '''
        with open('/dev/null', 'w') as devnull:
            subprocess.check_call('./test-remove-lpf', stdout=devnull)

    def test_build_fail(self):
        ''' Test build failure. '''
        with open('/dev/null', 'w') as devnull:
            subprocess.check_call('./test-build-fail', stdout=devnull)

    def test_notify(self):
        ''' Test notifications i. e., lpf-notify. '''
        with open('/dev/null', 'w') as devnull:
            subprocess.check_call(['/bin/bash', '-c', './test-notify'],
                                   stdout=devnull)

if __name__ == "__main__":
    unittest.main()

# vim: set expandtab ts=4 sw=4:
