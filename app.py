from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)

db = 'database.db'

conn = sqlite3.connect(db)
cursor = conn.cursor()

######### 메인페이지  #########
def get_user_by_id(user_id):
    query = "SELECT * FROM User WHERE user_id = ?"
    cursor.execute(query, (user_id))
    user = cursor.fetchone()
    return user

def get_user_categories(user_id):
    query = "SELECT category_id FROM Category WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    category_ids = cursor.fetchall()

    # 각 카테고리 ID에 해당하는 카테고리 정보 가져오기
    categories_todos = []

    for category_id in category_ids:
        data = []
        query = "SELECT * FROM category WHERE category_id = ?"
        cursor.execute(query, (category_id,))
        category_info = cursor.fetchone()
        data.append(category_info['name'])

        query = "SELECT * FROM TODO WHERE category_id = ?"
        cursor.execute(query, (category_id,))
        todos = cursor.fetchall()
        for todo in todos:
            data.append(todo['content'])

        categories_todos.append(data)

    return categories_todos



@app.route('/', methods=['GET'])
def index():  
    if 'user_id' in session:
        user_info = get_user_by_id(session['user_id'])
        categories_todos = get_user_categories(session['user_id'])
        ''
        

    user = {
        'nickname': user_info['nickname'],
        'name' : user_info['name'],
        'motto': user_info['motto'],
        'categories' : categories_todos
    }

    return render_template('index.html', data=user)


@app.route('/post', methods=['POST'])
def post():
    post_category = request.form['category']
    post_content = request.form['content']
    # db에 데이터 넣기
    cursor.execute('SELECT id FROM Category WHERE name = ?', (post_category))
    category_id = cursor.fetchone()  # 검색된 카테고리의 ID 가져오기
    cursor.execute('INSERT INTO (content, category_id) VALUES (?, ?)', (post_content, category_id))
    conn.commit()

    return redirect(url_for('index'))


######### 회원정보 조회 #########
@app.route('/user', method=['GET', 'POST'])
def user():
    if request.method=='GET':
        if 'user_id' in session:
            user_id = session['user_id']
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user_info = cursor.fetchone()  # fetchone()을 사용하여 해당 유저 정보를 가져옴

            if user_info:
                return render_template('profile.html', data=user_info)
            else:
                flash('User not found', 'error')

    if request.method == 'POST':
         if 'user_id' in session:
            user_id = session['user_id']
            new_motto = request.form['motto']
            # 사용자가 입력한 정보로 데이터베이스 업데이트
            cursor.execute("UPDATE users SET motto = ? WHERE user_id = ?", (new_motto, user_id))
            conn.commit()

            return redirect(url_for('user'))




######### 로그인/회원가입 페이지  #########
def login(userID, password):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM user WHERE user_id = ? AND password = ?
    ''', (userID, password))
    user = cursor.fetchone()

    return user

@app.route('/login', methods=['POST', 'GET'])
def login_route():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        user = login(user_id, password)
        if user:
            session['user_id'] = user_id
            # session['user'] = user
            flash('로그인 성공!', 'success')
            return redirect(url_for('index'))
        else:
            flash('로그인 실패. 다시 시도하세요.', 'danger')
            return redirect(url_for('login'))


def signup(userID, password, name, nickname):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO User (userID, password, name, nickname) VALUES (?, ?, ?, ?)
    ''', (userID, password, name, nickname))
    conn.commit()

@app.route('/signup', methods=['POST', 'GET'])
def signup_route():
    if request.method == 'POST':
        userID = request.form['userID']
        password = request.form['password']
        name = request.form['name']
        nickname = request.form['nickname']
        signup(userID, password, name, nickname)
        flash('회원가입 성공! 로그인하세요.', 'success')
        
        return redirect(url_for('index'))
    
    if request.method == 'GET':
        return render_template('signup.html')

# @app.route('/main')
# def main():
#     if 'user' in session:
#         return render_template('main.html')
#     else:
#         flash('로그인이 필요합니다.', 'danger')
#         return redirect(url_for('index'))
        

if __name__ == '__main__':
    app.run(debug=True)



