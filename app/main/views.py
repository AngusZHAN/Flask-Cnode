from . import main
from .. import db
from ..models import (
    User,
    Topic,
    Reply,
)
from flask import (
    render_template,
    redirect,
    request,
    url_for,
    flash,
    session,
)
from flask_login import (
    login_required,
    login_user,
    logout_user,
    current_user,
)

@main.route('/')
@main.route('/index/')
def index():
    topics = Topic.query.order_by('-create_time').all()
    return render_template('index.html', topics=topics)


@main.route('/<int:id>')
def detail(id):
    topic_model = Topic.id
    return render_template('detail.html', topic=topic_model)


@main.route('/publish/', methods=['GET','POST'])
@login_required
def publish():
    form = request.form
    if request.method == 'POST':
        topic = Topic(title=form.get('title'),
                      body=form.get('body'),
                      author=current_user._get_current_object())
        db.session.add(topic)
        db.session.commit()
        flash('发布成功')
        return redirect(url_for('.index'))
    return render_template('publish.html', form=form)
