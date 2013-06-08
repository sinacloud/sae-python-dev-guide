#!/usr/bin/env python
# -*-coding: utf8 -*-

"""Task Queue API
TaskQueue is a distributed task queue service provided by SAE for developers as
a simple way to execute asynchronous user tasks.

Example:

1. Add a GET task.
    
    from sae.taskqueue import Task, TaskQueue

    queue = TaskQueue('queue_name')
    queue.add(Task("/tasks/cd"))

2. Add a POST task.

    queue.add(Task("/tasks/strip", "postdata"))

3. Add a bundle of tasks.

    tasks = [Task("/tasks/grep", d) for d in datas]
    queue.add(tasks)

4. A simple way to add task.

    from sae.taskqueue import add_task
    add_task('queue_name', '/tasks/fsck', 'postdata')
"""

__all__ = ['Error', 'InternalError', 'InvalidTaskError', 
           'PermissionDeniedError', 'TaskQueueNotExistsError', 
           'TooManyTasksError', 'add_task', 'Task', 'TaskQueue']

import os
import time
import json
import urllib
import urllib2
import urlparse
import base64

import util
import const

class Error(Exception):
    """Base-class for all exception in this module"""

class InvalidTaskError(Error):
    """The task's url, payload, or options is invalid"""

class InternalError(Error):
    """There was an internal error while accessing this queue, it should be 
    temporary, it problem continues, please contact us"""

class PermissionDeniedError(Error):
    """The requested operation is not allowed for this app"""

class TaskQueueNotExistsError(Error):
    """The specified task queue does not exist"""

class TooManyTasksError(Error):
    """Either the taskqueue is Full or the space left's not enough"""

_ERROR_MAPPING = {
    1: PermissionDeniedError, 3: InvalidTaskError, 10: TaskQueueNotExistsError,
    11: TooManyTasksError, 500: InternalError, #999: UnknownError,
    #403: Permission denied or out of quota 
}

_TASKQUEUE_BACKEND = 'http://taskqueue.sae.sina.com.cn/index.php'

class Task:

    _default_netloc = 'http://' + os.environ['HTTP_HOST']

    def __init__(self, url, payload = None, **kwargs):
        """Initializer.

        Args:
          url: URL where the taskqueue daemon should handle this task.
          payload: Optinal, if provided, the taskqueue daemon will take this 
            task as a POST task and |payload| as POST data.
          delay: Delay the execution of the task for certain second(s). Up to
            600 seconds.
          prior: If set to True, the task will be add to the head of the queue.

        Raises:
          InvalidTaskError: if there's a unrecognized argument.
        """
        self.info = {}
        if url.startswith('http://'):
            self.info['url'] = url
        else:
            self.info['url'] = urlparse.urljoin(self._default_netloc, url)
        if payload:
            self.info['postdata'] = base64.b64encode(payload)
                
        for k, v in kwargs.iteritems():
            if k == 'delay':
                self.info['delay'] = v
            elif k == 'prior':
                self.info['prior'] = v
            else:
                raise InvalidTaskError()

    def extract_params(self):
        return self.info

class TaskQueue:

    def __init__(self, name, auth_token=None):
        """Initializer.

        Args:
          name: The name of the taskqueue.
          auth_token: Optional, a two-element tuple (access_key, secretkey_key),
            useful when you want to access other application's taskqueue.
        """
        self.name = name

        if auth_token: 
            self.accesskey_key, self.secret_key = auth_token
        else:
            self.access_key = const.ACCESS_KEY
            self.secret_key = const.SECRET_KEY

    def add(self, task):
        """Add task to the task queue

        Args:
          task: The task to be added, it can be a single Task, or a list of 
            Tasks.
        """
        try:
            tasks = list(iter(task))
        except TypeError:
            tasks = [task]

        task_args = {}
        task_args['name'] = self.name
        task_args['queue'] = []
        for t in tasks:
            task_args['queue'].append(t.extract_params())

        #print task_args
        args = [('taskqueue', json.dumps(task_args))]

        return self._remote_call(args)

    def size(self):
        """Query for how many task is left(not executed) in the queue. """
        args = []
        args.append(('act', 'curlen'))
        args.append(('params', json.dumps({'name': self.name})))
        return int(self._remote_call(args))

    def _remote_call(self, args):
        args_dict = dict(args)

        command = args_dict.get('act')
        if command == 'curlen':
            return "0"

        tasks = json.loads(args_dict['taskqueue'])['queue']
        for t in tasks:
            url = t['url']
            payload = t.get('postdata')

            if payload:
                payload = base64.b64decode(payload)
            print '[SAE:TASKQUEUE] Add task:', url, payload

            #try:
            #    # Try to make a sync call.
            #    rep = urllib2.urlopen(url, payload, 5)
            #    print rep.read()
            #except:
            #    import traceback
            #    print 'TASKQUEUE_ERROR:', t    
            #    traceback.print_exc()

        return True

    def _get_headers(self):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        msg = 'ACCESSKEY' + self.access_key + 'TIMESTAMP' + timestamp
        headers = {'TimeStamp': timestamp,
                   'AccessKey': self.access_key,
                   'Signature': util.get_signature(self.secret_key, msg)}

        return headers

def add_task(queue_name, url, payload=None, **kws):
    """A shortcut for adding task
    
    Args:
      queue_name: The queue's name of which you want the task be added to.
      url: URL where the taskqueue daemon should handle this task.
      payload: The post data if you want to do a POST task.
    """
    TaskQueue(queue_name).add(Task(url, payload, **kws))
