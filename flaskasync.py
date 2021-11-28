# https://stackoverflow.com/questions/40989671/background-tasks-in-flask

import threading
import uuid
from functools import wraps

from flask import current_app, request, abort
from werkzeug.exceptions import HTTPException, InternalServerError

flask_async_tasks = {}

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
				except HTTPException as e:
					flask_async_tasks[task_id]["result"] = current_app.handle_http_exception(e)
				except Exception as e:
					# The function raised an exception, so we set a 500 error
					flask_async_tasks[task_id]["result"] = InternalServerError()
					if current_app.debug:
						# We want to find out if something happened so reraise
						raise

		# Assign an id to the asynchronous task
		task_id = uuid.uuid4().hex

		# Record the task, and then launch it
		flask_async_tasks[task_id] = {"task": threading.Thread(
			target=task, args=(current_app._get_current_object(), request.environ))}
		flask_async_tasks[task_id]["task"].start()
		print("new task started ", task_id)

		# Return a 202 response, with an id that the client can use to obtain task status
		return {"TaskId": task_id}, 202

	return wrapped

def flask_async_result(task_id = None):
	# Return results of asynchronous task.
	# If this request returns a 202 status code, it means that task hasn't finished yet.
	if task_id:
		task = flask_async_tasks.get(task_id)
	elif len(flask_async_tasks) == 1:
		task = list(flask_async_tasks)[0]
	else:
		task = None
	if task is None:
		abort(404)
	if "result" not in task:
		return {"TaskID": task_id}, 202
	return task["result"]
