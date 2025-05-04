from flask import render_template, request, Blueprint
from flaskstart.models import Post

main = Blueprint('main', __name__) # instance of Blueprint

########## MAIN PAGE ##########
@main.route("/") # декоратор, в цьому випадку реєструє маршрут на головну сторінку, після чого виконує клас/ф-цію знизу
@main.route("/home") # ще один декоратор, з іншим шляхом але веде на цю ж саму сторінку
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    # picturesRead = Support.query.all()
    # form = UpdateAccountForm()
    
    # if form.validate_on_submit():
    #     if form.picture.data:
    #         picture_file = save_picture_text(form.picture.data)
    #         current_user.image_file = picture_file
    # 
    # return render_template("home.html", postsRead=posts, picturesRead=picturesRead)

    return render_template("home.html", postsRead=posts)



@main.route("/about") # ще один декоратор але з іншим шляхом, до сторінки про нас
def about():
    return render_template("about.html", title="Про Нас")

