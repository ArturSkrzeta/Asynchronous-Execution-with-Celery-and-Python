<h2>Asynchronous Execution with Celery and Python</h2>
<h3>Celery Architecture</h3>
<ul>
  <li>client app --> message queue in taks broker --> worker --> result storage --> client</li>
  <br>
  <img src="images/architecture.JPG">
  <li>The data result storage generates the task ID so that client can track its status.</li>
  <li>For tasks broker I can choose</li>
  <li>For passing a function to the celery, the only thing you need to do is put the decorator '@app.task' above the function.</li>
</ul>
