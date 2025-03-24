from flask import Flask, request, render_template_string
import pymysql.cursors
import os

app = Flask(__name__)

@app.after_request
def enforce_utf8(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

# Конфигурация базы данных
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'db': os.getenv('DB_NAME'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# HTML шаблоны с оформлением
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>CyberCTF Blog</title>
    <style>
        :root {{
            --primary: #2ecc71;
            --dark: #1a1a1a;
            --light: #ecf0f1;
            --danger: #e74c3c;
        }}
        
        body {{
            font-family: 'Segoe UI', system-ui;
            background: var(--dark);
            color: var(--light);
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .header {{
            border-bottom: 2px solid var(--primary);
            padding-bottom: 15px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            font-size: 2em;
            color: var(--primary);
            text-decoration: none;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(46, 204, 113, 0.3);
        }}
        
        .nav-link {{
            padding: 10px 20px;
            border-radius: 5px;
            transition: all 0.3s;
            margin-left: 15px;
        }}
        
        .nav-link:hover {{
            background: rgba(46, 204, 113, 0.1);
            transform: translateY(-2px);
        }}
        
        .article {{
            background: #2a2a2a;
            border-radius: 8px;
            padding: 25px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 4px solid var(--primary);
        }}
        
        .article h2 {{
            color: var(--primary);
            margin-top: 0;
        }}
        
        .article-meta {{
            color: #95a5a6;
            font-size: 0.9em;
            margin-bottom: 15px;
        }}
        
        .error {{
            background: var(--danger);
            color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        
        .search-box {{
            background: #333;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        
        .search-form {{
            display: flex;
            gap: 10px;
        }}
        
        input[type="text"] {{
            flex: 1;
            padding: 10px;
            background: #404040;
            border: 1px solid #555;
            color: var(--light);
            border-radius: 5px;
        }}
        
        button {{
            background: var(--primary);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        button:hover {{
            background: #27ae60;
            box-shadow: 0 0 15px rgba(46, 204, 113, 0.3);
        }}
        
        .login-form {{
            background: #333;
            padding: 40px;
            border-radius: 10px;
            max-width: 400px;
            margin: 50px auto;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
        }}
        
        .login-form input {{
            width: 100%;
            margin-bottom: 15px;
            padding: 12px;
            background: #404040;
            border: 1px solid #555;
            color: var(--light);
        }}
        
        .login-form button {{
            width: 100%;
            padding: 12px;
        }}
    </style>
</head>
<body>
    <header class="header">
        <a href="/" class="logo">CyberCTF</a>
        <nav>
            <a href="/login" class="nav-link">🔐 Admin Panel</a>
        </nav>
    </header>
    <div class="search-box">
        <form action="/" class="search-form">
            <input type="text" name="article_id" placeholder="Enter article ID or SQL query...">
            <button type="submit">Search</button>
        </form>
    </div>
    {}
</body>
</html>
'''

ARTICLE_TEMPLATE = '''
<div class="article">
    <div class="article-meta">
        Article ID: {{ article_id }} | Category: Hacking
    </div>
    <h2>{{ title }}</h2>
    <p>{{ text }}</p>
</div>
'''

@app.route('/')
def index():
    article_id = request.args.get('article_id')
    connection = None
    content = '<h1>Latest Articles</h1>'
    
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            if not article_id:
                cursor.execute("SELECT id, title FROM articles ORDER BY id DESC")
                articles = cursor.fetchall()
                content += ''.join([f'<div><a href="/?article_id={a["id"]}">{a["title"]}</a></div>' for a in articles])
                return HTML_TEMPLATE.format(content)
            
            sql = f"SELECT * FROM articles WHERE id = {article_id}"
            cursor.execute(sql)
            result = cursor.fetchone()
            
            if result:
                article_html = render_template_string(
                    ARTICLE_TEMPLATE,
                    title=result['title'],
                    text=result['text'],
                    article_id=article_id
                )
                content += article_html
            else:
                content += '<p>Article not found</p>'
                
    except Exception as e:
        content += f'<div class="error">Error: {str(e)}</div>'
    finally:
        if connection:
            connection.close()
    
    return HTML_TEMPLATE.format(content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = None
        try:
            connection = pymysql.connect(**db_config)
            with connection.cursor() as cursor:
                sql = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
                cursor.execute(sql)
                if cursor.fetchone():
                    return "Flag: CTF{Uni0n_S3l3ct_1s_P0wer}"
                return HTML_TEMPLATE.format('<div class="error">Invalid credentials</div>')
        except Exception as e:
            return HTML_TEMPLATE.format(f'<div class="error">{str(e)}</div>')
        finally:
            if connection:
                connection.close()
    
    return HTML_TEMPLATE.format('''
        <div class="login-form">
            <h2>🔒 Admin Login</h2>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Authenticate</button>
            </form>
        </div>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
