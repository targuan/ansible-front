import threading
from Queue import Queue, Empty
import subprocess


class Runner:
    def __init__(self, workers = 5):
        self.workers = workers
        self._queue = Queue()
        self._running_workers = []
        self._continue = True
    
    def put(self, job):
        self._queue.put(job)
    
    def run(self):
        for i in xrange(self.workers):
            worker = threading.Thread(target=self.process_jobs)
            worker.daemon = False
            worker.start()
            self._running_workers.append(worker)
    
    def stop(self):
        self._continue = False
    
    def process_jobs(self):
        while self._continue:
            try:
                job_id = self._queue.get(True, 1)
                print "Running " + str(job_id)
                job = ["ansible-playbook","--list-tasks"]
                p = subprocess.Popen(job,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                stdoutdata, stderrdata = p.communicate()
                print "Job ran: "+stdoutdata + stderrdata
                self._queue.task_done()
            except Empty:
                pass
            except:
                print "Oups"
                