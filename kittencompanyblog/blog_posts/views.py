from flask import abort, render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from kittencompanyblog import db 
from kittencompanyblog.models import BlogPost
from kittencompanyblog.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts', __name__)

#CREATE BLOGPOST
@blog_posts.route('/create', methods=["GET","POST"])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        print("form validated")

        blog_post = BlogPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id
                             )
        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('core.index'))
    else:
        print(form.errors)

    return render_template('create_post.html',form=form)


#VIEW BLOGPOST
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', 
                           title=blog_post.title,
                           date=blog_post.date,
                           post=blog_post
                           )



#UPDATE
@blog_posts.route('/<int:blog_post_id>/update', methods=["GET","POST"])
@login_required
def update(blog_post_id):
    #make sure author = current user:
    post = BlogPost.query.get_or_404(blog_post_id)

    if post.author != current_user:
        abort(403)

    form = BlogPostForm()
    if form.validate_on_submit():
        post.title = form.title.data 
        post.text = form.text.data
        post.user_id = current_user.id
        # commit to database (because it's an update):
        db.session.commit()
        flash('Blog Post Updated')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=blog_post_id))


    elif request.method == 'GET':    
        form.title.data = post.title
        form.text.data = post.text

    return render_template('create_post.html', title="Updating", form=form, post=post)


#DELETE
@blog_posts.route('/<int:blog_post_id>/delete', methods=["GET","POST"])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    
    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted')

    return redirect(url_for('core.index'))
