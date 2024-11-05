from flask import Flask, session, request
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

word_list = [
    'a', 'am', 'and', 'anywhere', 'are', 'be', 'boat', 'box', 'car', 'could',
    'dark', 'do', 'eat', 'eggs', 'fox', 'goat', 'good', 'green', 'ham', 'here',
    'house', 'I', 'if', 'in', 'let', 'like', 'may', 'me', 'mouse', 'not', 'on',
    'or', 'rain', 'Sam', 'say', 'see', 'so', 'thank', 'that', 'the', 'them',
    'there', 'they', 'train', 'tree', 'try', 'will', 'with', 'would', 'you'
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'word_list' not in session:
        shuffled_words = word_list.copy()
        random.shuffle(shuffled_words)
        session['word_list'] = shuffled_words
        session['word_index'] = 0
    else:
        if request.method == 'POST':
            session['word_index'] += 1

    word_index = session.get('word_index', 0)
    shuffled_words = session.get('word_list', [])

    if word_index >= len(shuffled_words):
        # End of list reached
        return '''
        <!doctype html>
        <html>
        <head>
            <title>Flashcard</title>
            <style>
                body {
                    margin: 0;
                    padding: 0;
                    background-color: #fff;
                }
                .message {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-size: 8vw;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <div class="message">End of words.<br>Thank you!</div>
        </body>
        </html>
        '''

    current_word = shuffled_words[word_index]

    # Render the word in large font, and make the entire screen clickable
    html = f"""
    <!doctype html>
    <html>
    <head>
        <title>Flashcard</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #fff;
            }}
            .container {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .word {{
                font-size: 10vw;
                text-align: center;
            }}
        </style>
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                document.body.addEventListener('click', function() {{
                    document.getElementById('next_form').submit();
                }});
            }});
        </script>
    </head>
    <body>
        <div class="container">
            <div class="word">{current_word}</div>
        </div>
        <form id="next_form" method="post" action="/">
        </form>
    </body>
    </html>
    """

    return html

if __name__ == '__main__':
    app.run(debug=True)