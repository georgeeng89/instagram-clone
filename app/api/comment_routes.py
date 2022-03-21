from flask import Blueprint, jsonify, session, request
from flask_login import login_required
from app.models import db, Photo, Comment
from app.forms import AddPhotoForm, EditPhotoForm, AddCommentForm
from flask_login import current_user, login_required


comment_routes = Blueprint('comments', __name__)


def validation_errors_to_error_messages(validation_errors):
    """
    Simple function that turns the WTForms validation errors into a simple list
    """
    errorMessages = []
    for field in validation_errors:
        for error in validation_errors[field]:
            errorMessages.append(f'{field} : {error}')
    return errorMessages


@comment_routes.route('/')
# @login_required
def comments():
  comments = Comment.query.all()
  return jsonify([comment.to_dict() for comment in comments])


@comment_routes.route('/add', methods=['POST'])
# @login_required
def add_comment():
    """
    POSTS A COMMENT
    """
    form = AddCommentForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        comment = Comment(
            user_id=form.data['user_id'],
            photo_id=form.data['photo_id'],
            content=form.data['content']
        )

        db.session.add(comment)
        db.session.commit()

        return comment.to_dict()

    return {'errors': validation_errors_to_error_messages(form.errors)}, 401



# @photo_routes.route('/delete/<int:id>', methods=['DELETE'])
# # @login_required
# def remove_photo(id):
#     photo = Photo.query.get(id)

#     if(current_user.id == photo.user_id):
#         db.session.delete(photo)
#         db.session.commit()

#     return "Photo Deleted Successfully"



# @photo_routes.route('/edit/<int:id>', methods=['PUT'])
# @login_required
# def update_photo(id):
#     photo = Photo.query.get(id)

#     form = EditPhotoForm()
#     form['csrf_token'].data = request.cookies['csrf_token']

#     if form.validate_on_submit():

#         photo.user_id = form.data['user_id']
#         photo.caption = form.data['caption']
#         photo.url = form.data['url']

#         try:
#             db.session.add(photo)
#             db.session.commit()

#             return photo.to_dict()

#         except:

#             return {'errors': ['Photos : Something went wrong. Please try again']}, 401

#     return {'errors': validation_errors_to_error_messages(form.errors)}, 401