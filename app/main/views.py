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


@main.route('/detail/<topic_id>')
def detail(topic_id):
    topic_model = Topic.query.filter(Topic.id == topic_id).first()
    replies = Reply.query.filter_by(topic_id = topic_id).all()
    return render_template('detail.html', topic=topic_model, replies=replies)


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


@main.route('/reply/<topic_id>', methods=['GET','POST'])
@login_required
def reply(topic_id):
    form = request.form
    if request.method == 'POST':
        reply = Reply(body=form.get('body'),
                      topic_id=topic_id,
                      author=current_user._get_current_object())
        db.session.add(reply)
        db.session.commit()
        flash('回复成功')
        return redirect(url_for('.detail', topic_id=topic_id))
    return render_template('reply.html', form=form, topic_id=topic_id)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    topic = Topic.query.get_or_404(id)
    if current_user != topic.author:
        flash('您不是话题作者，无法修改。')
        return redirect(url_for('.detail', topic_id=id))
    form = request.form
    if request.method == 'POST':
        topic = Topic(body=form.get('body'))
        db.session.add(topic)
        db.session.commit()
        flash('文章修改成功')
        return redirect(url_for('.detail', topci_id=Topic.id))
    Topic(body=topic.body)
    return render_template('edit_topic.html', form=form)


@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    # posts = user.posts.order_by().all
    return render_template('user.html', user=user)


@main.route('/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = request.form
    if request.method == 'POST' and form.validate():
        current_user.name = form.get('name')
        current_user.location = form.get('location')
        current_user.about_me = form.get('about_me')
        db.session.add(current_user)
        db.session.commit()
        flash('修改资料成功')
        return redirect(url_for('.user', username=current_user.username))
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/up_avatar/', methods=['GET', 'POST'])
@login_required
def up_avatar():
    avatar = request.files.get('file')
    fname = avatar.filename
    UPLOAD_FOLDER = "D:\\Code\\Flask-Cnode\\app\\static\\avatar\\"
    ALLOWED_EXTENSIONS = ['gif', 'png', 'jpg', 'jpeg']
    flag = '.' in fname and fname.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    if not flag:
        flash('文件类型错误，请重试')
        return redirect(url_for('.user', username=current_user.username))
    avatar.save('{}{}_{}'.format(UPLOAD_FOLDER, current_user.username, fname))
    current_user.i_avatar = '\\static\\avatar\\{}_{}'.format(
                                                current_user.username, fname)
    db.session.add(current_user)
    db.session.commit()
    flash('上传头像成功')
    return redirect(url_for('.user', username=current_user.username))