from aiohttp import web
from fastapi.encoders import jsonable_encoder

from repositories import TodoRepo


class Tools:
    def isEmpty(todo: []):
        if len(todo) == 0:
            return True
        else:
            return False

    def encoderJson(obj):
        return jsonable_encoder(obj)

    def finalResponse(obj):
        return web.json_response(obj)

    def errorNotFound(obj):
        error = ('%s not found', obj)
        return {'error': error}

    def getCompleted(session, data, todoEncoded, id):
        if 'completed' not in data:
            return TodoRepo.fetch_get_completed(session, id)
        else:
            return todoEncoded['completed']

    def getOrder(session, data, todoEncoded, id):
        if 'order' not in data:
            return TodoRepo.fetch_get_order(session, id)
        else:
            return todoEncoded['order']

    def getUrl(session, data, encoded, id, repo):
        if 'url' not in data:
            return repo.fetch_get_url(session, id)
        else:
            return encoded['url']

    def getTitle(session, data, encoded, id, repo):
        if 'title' not in data:
            return repo.fetch_get_title(session, id)
        else:
            return encoded['title']
