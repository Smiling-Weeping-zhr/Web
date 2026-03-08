import ipdb
from flask import abort, render_template, request, jsonify, session
from ..models import Dataset
from flask_login import current_user, login_required
from .. import db
from .utils import chat_with_ai
from .forms import DownloadSearchForm
from . import home

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

# add sorting, filtering, and pagination view
@home.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    form = DownloadSearchForm(request.args)
    query = Dataset.search(form)
    # 分页
    page = request.args.get('page', 1, type=int)
    pagination = query.paginate(page=page, per_page=10)

    datasets = pagination.items

    return render_template(
        'home/dashboard.html',
        form=form,
        data=datasets,
        pagination=pagination,
        title="Dashboard"
    )

@home.route('/articles', methods=["GET"])
@login_required
def articles():
    return render_template('home/articles.html', title="Articles")

@home.route('/chat', methods=["GET"])
@login_required
def chat_page():
    return render_template('home/chat.html', title="AI Assistant")

@home.route('/api/chat', methods=["POST"])
@login_required
def chat_api():
    data = request.get_json() # {'message': 'hello'}
    user_message = data["message"]
    history = session.get("chat_history", []) # History is stored in session
    reply, history = chat_with_ai(user_message, history)
    # 保存回 session
    session["chat_history"] = history
    return jsonify({"reply": reply})