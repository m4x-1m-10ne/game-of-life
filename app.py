from flask import Flask, render_template, request, session, redirect, url_for
import random
import time

app = Flask(__name__)
app.secret_key = 'your-secret-key'

def empty_grid(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

def random_grid(rows, cols):
    return [[random.choice([0, 1]) for _ in range(cols)] for _ in range(rows)]

def next_generation(grid):
    rows = len(grid)
    cols = len(grid[0])
    new_grid = [[0]*cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            # подсчет соседей
            neighbors = 0
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        neighbors += grid[ni][nj]
            if grid[i][j] == 1:
                if neighbors in [2, 3]:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
            else:
                if neighbors == 3:
                    new_grid[i][j] = 1
    return new_grid

def grid_is_dead(grid):
    return all(cell == 0 for row in grid for cell in row)

@app.route('/', methods=['GET', 'POST'])
def index():
    rows = 20
    cols = 20
    if 'grid' not in session:
        session['grid'] = random_grid(rows, cols)
        session['generation'] = 0
        session['running'] = False

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'start':
            session['running'] = True
        elif action == 'stop':
            session['running'] = False
        elif action == 'clear':
            session['grid'] = empty_grid(rows, cols)
            session['generation'] = 0
            session['running'] = False
        elif action == 'random':
            session['grid'] = random_grid(rows, cols)
            session['generation'] = 0
            session['running'] = False
        elif action == 'step':
            if session['running']:
                # если уже running, то step не нужен, обрабатывается отдельно
                pass
            else:
                session['grid'] = next_generation(session['grid'])
                session['generation'] += 1
                if grid_is_dead(session['grid']):
                    session['running'] = False
        # Для автоматического шага при running
        if session.get('running'):
            session['grid'] = next_generation(session['grid'])
            session['generation'] += 1
            if grid_is_dead(session['grid']):
                session['running'] = False
        session.modified = True
        return redirect(url_for('index'))

    return render_template('index.html', grid=session['grid'], generation=session['generation'], running=session.get('running', False))

if __name__ == '__main__':
    app.run(debug=True)