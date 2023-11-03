from flask import Flask, request, render_template, redirect, url_for, flash, g
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
task = {}
task_file = 'tasks.txt'


def get_tasks():
    try:
        with open(task_file, 'r') as file:
            tasks = file.read().splitlines()
        return tasks
    except FileNotFoundError:
        return []


def save_tasks(tasks):
    with open(task_file, 'w') as file:
        file.write('\n'.join(tasks))


@app.route('/')
def index():
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add():
    new_task = request.form['task']
    tasks = get_tasks()
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect(url_for('index'))


@app.route('/remove', methods=['POST'])
def remove():
    task_to_remove = request.form['task']
    tasks = get_tasks()

    if task_to_remove in tasks:
        tasks.remove(task_to_remove)
        save_tasks(tasks)

    return redirect('/')


# # This block is necessary when you run the app directly (not during testing)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
