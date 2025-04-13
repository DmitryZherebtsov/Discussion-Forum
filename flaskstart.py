from flask import Flask # імпорт класу Flask з бібліотеки flask
from flask import render_template
from flask import url_for
from forms import RegitratioinForm, LoginForm


app = Flask(__name__) # екземпляр застосунку під назвою app

app.config['SECRET_KEY'] = 'ce9b10bbc3ba4db3e0b1b5274d1a0517'

postsByUsers = [
    {
        'author': 'Homer',
        'title': 'Strange Philosophy of Human Being',
        'content': "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.",
        'date': 'June, 8th century BCE'
    },
    {
        'author': 'Aristotle',
        'title': 'Strange Philosophy of Homer Being',
        'content': "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged.",
        'date': 'February, 	322 BC'
    }
]



@app.route("/") # декоратор, в цьому випадку реєструє маршрут на головну сторінку, після чого виконує клас/ф-цію знизу
@app.route("/home") # ще один декоратор, з іншим шляхом але веде на цю ж саму сторінку
def home():
    return render_template("home.html", postsRead=postsByUsers)


@app.route("/about") # ще один декоратор але з іншим шляхом, до сторінки про нас
def about():
    return render_template("about.html", title="Про Нас")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegitratioinForm()
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__": # перевірка того чи запускаємо ми сервак на пряму 
    app.run(debug=True) # запускає сервер і виводить дебаг у браузер, також реагує на зміни
else:
    print("Сервер НЕ ЗАПУСТИВСЯ!")
