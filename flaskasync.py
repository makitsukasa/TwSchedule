# https://stackoverflow.com/questions/40989671/background-tasks-in-flask

import threading
import uuid
from functools import wraps
from datetime, import datetime, timedelta

from flask import current_app, request, abort
from werkzeug.exceptions import HTTPException, InternalServerError

LOG_SIZE = 500
TIMEDELTA = timedelta(days = 1)
flask_async_tasks = {}

def get_timestamp():
	return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def thin_out_log():
	if len(flask_async_tasks) < LOG_SIZE:
		return
	threshold = (datetime.now() - TIMEDELTA).strftime("%Y/%m/%d %H:%M:%S")
	old_keys = []
	for k, v in flask_async_tasks.items():
		if v["start_timestamp"] < threshold:
			old_keys.append(k)
	for k in old_keys:
		del flask_async_tasks[k]

def flask_async(f):
	# This decorator transforms a sync route to asynchronous by running it in a background thread.
	@wraps(f)
	def wrapped(*args, **kwargs):
		def task(app, environ):
			# Create a request context similar to that of the original request
			with app.request_context(environ):
				try:
					# Run the route function and record the response
					flask_async_tasks[task_id]["result"] = f(*args, **kwargs)		
					flask_async_tasks[task_id]["end_timestamp"] = get_timestamp()
				except HTTPException as e:
					flask_async_tasks[task_id]["result"] = current_app.handle_http_exception(e)
					flask_async_tasks[task_id]["end_timestamp"] = get_timestamp()
				except Exception as e:
					# The function raised an exception, so we set a 500 error
					flask_async_tasks[task_id]["result"] = InternalServerError()
					flask_async_tasks[task_id]["end_timestamp"] = get_timestamp()
					if current_app.debug:
						# We want to find out if something happened so reraise
						raise

		# Assign an id to the asynchronous task
		task_id = uuid.uuid4().hex

		# Record the task, and then launch it
		flask_async_tasks[task_id] = {"task": threading.Thread(
			target=task, args=(current_app._get_current_object(), request.environ))}
		flask_async_tasks[task_id]["start_timestamp"] = get_timestamp()
		flask_async_tasks[task_id]["task"].start()
		print("new task started ", task_id)
		
		thin_out_log()		

		# Return a 202 response, with an id that the client can use to obtain task status
		return {"taskid": task_id}, 202

	return wrapped

def flask_async_log(task_id = None):
	# Return logs of asynchronous task.
	# If this request returns a 202 status code, it means that task hasn't finished yet.
	if task_id:
		tasks = [flask_async_tasks.get(task_id)]
	elif len(flask_async_tasks) == 0:
		return "no task has run yet", 404
	else:
		tasks = sorted(list(flask_async_tasks.values()), key = lambda i: i["start_timestamp"], reverse = True)
	if not tasks or tasks[0] is None:
		return "broken or invalid task", 404
	ret = ""
	for task in tasks:
		if "result" not in task:
			ret += f'{task["start_timestamp"]} - still running<br>'
		else:
			end = task["end_timestamp"].split[" "][1]
			ret += f'{task["start_timestamp"]} - {end} {task["result"]}<br>'
	return ret
