import src
from src.controllers import main_controller
from src import util


@src.app.route('/models/<username>/', methods=['GET'])
@util.exc_handler
def search_model(username):
    model = main_controller.search_model(username)
    if not model:
        raise util.WebExeception('model not found', 404)
    return {'model': model}, 200


@src.app.route('/recommendations/<username>/<anime_id>/', methods=['GET'])
@util.exc_handler
def search_recommendation(username, anime_id):
    rec = main_controller.search_recommendation(username, anime_id)
    if not rec:
        raise util.WebExeception('recommendation not found', 404)
    return {'recommendation': rec}, 200
