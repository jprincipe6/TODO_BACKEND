from aiohttp import web
from fastapi.encoders import jsonable_encoder

from db import session
from repositories import TodoRepo, Relation, TagRepo
from utilities import Tools


class Todos:

    async def get_all_todos(request):
        todo_f = TodoRepo.fetch_all(session)
        if Tools.isEmpty(todo_f) is True:
            return Tools.finalResponse([])
        else:
            finalResponse = []
            for i in range(len(todo_f)):
                todoFinal = Tools.encoderJson(todo_f[i])
                tags = Relation.fetch_all_by_id_todo(session, todoFinal['id'])
                tagFinal = Tools.encoderJson(tags)
                if Tools.isEmpty(tagFinal) is True:
                    finalResponse.append(todoFinal)
                else:
                    todoFinal["tags"] = tagFinal
                    finalResponse.append(todoFinal)
            return Tools.finalResponse(finalResponse)

    async def get_one_todo(request):
        id = request.match_info['id']
        todo = TodoRepo.fetch_by_id(session, id)
        exists = TodoRepo.fecth_is_exists(session, id)
        if exists == False:
            return Tools.finalResponse(Tools.errorNotFound('Todo'), status=404)
        tags = Relation.fetch_all_by_id_todo(session, id)
        todoFinal = Tools.encoderJson(todo)
        tagFinal = Tools.encoderJson(tags)
        if Tools.isEmpty(tags) is True:
            todoFinal["tags"] = []
        else:
            todoFinal["tags"] = tagFinal
        return Tools.finalResponse(todoFinal)

    async def update_todo(request):
        id = int(request.match_info['id'])
        exists = TodoRepo.fecth_is_exists(session, id)
        if exists == False:
            return Tools.encoderJson(Tools.errorNotFound('Todo'))

        data = await request.json()
        todoEncoded = jsonable_encoder(data)

        completed = Tools.getCompleted(session, data, todoEncoded, id)
        order = Tools.getOrder(session, data, todoEncoded, id)
        url = Tools.getUrl(session, data, todoEncoded, id, TodoRepo)
        title = Tools.getTitle(session, data, todoEncoded, id, TodoRepo)

        todo = TodoRepo.fetch_by_id(session, id)
        todoFinal = {}
        todo.id = id
        todo.title = title
        todo.completed = completed
        todo.order = order
        todo.url = url
        await TodoRepo.update(session, todo_data=todo)
        todoFinal['id'] = id
        todoFinal['title'] = todo.title
        todoFinal['completed'] = todo.completed
        todoFinal['order'] = todo.order
        todoFinal['url'] = todo.url
        return Tools.finalResponse(todoFinal)

    async def create_todo(request):
        data = await request.json()

        if 'title' not in data:
            return Tools.finalResponse({'error': '"title" is a required field'})
        title = data['title']
        if not isinstance(title, str) or not len(title):
            return Tools.finalResponse({'error': '"title" must be a string with at least one character'})

        data['completed'] = bool(data.get('completed', False))
        new_id = TodoRepo.fetch_get_last_key(session) + 1
        data['url'] = str(request.url.join(request.app.router['one_todo'].url_for(id=str(new_id))))
        if 'order' not in data:
            order = None
        else:
            order = data['order']

        await TodoRepo.create(session, new_id, title, data['completed'], order, data['url'])

        return web.Response(
            headers={'Location': data['url']},
            status=303
        )

    async def remove_all_todos(request):
        await Relation.delete_all(session)
        await TodoRepo.delete_all(session)
        return web.Response(status=204)

    async def remove_todo(request):
        id = int(request.match_info['id'])
        exists = TodoRepo.fecth_is_exists(session, id)
        if exists == False:
            return Tools.finalResponse(Tools.errorNotFound('Todo'))
        await TodoRepo.delete(session, id)
        return web.Response(status=204)


class Tags:
    async def get_all_tags(request):
        tags = TagRepo.fetch_all(session)
        if Tools.isEmpty(tags) is True:
            return Tools.finalResponse([])
        else:
            tags = Tools.encoderJson(tags)
            finalResponse = []
            for tag in tags:
                todos = Relation.fetch_all_by_id_tag(session, tag['id'])
                todosEncoder = Tools.encoderJson(todos)
                if Tools.isEmpty(todos) is True:
                    tag['todos'] = []
                    finalResponse.append(tag)
                else:
                    tag['todos'] = todosEncoder
                    finalResponse.append(tag)
        return web.json_response(finalResponse)

    async def get_one_tag(request):
        id = request.match_info['id']
        tag = TagRepo.fetch_by_id(session, id)
        exists = TagRepo.fecth_is_exists(session, id)
        if exists == False:
            return Tools.finalResponse(Tools.errorNotFound('Tags'), status=404)
        todos = Relation.fetch_all_by_id_tag(session, id)
        todosFinal = Tools.encoderJson(todos)
        tagFinal = jsonable_encoder(tag)
        if Tools.isEmpty(todos) is True:
            tagFinal['todos'] = []
        else:
            tagFinal['todos'] = todosFinal
        return Tools.finalResponse(tagFinal)

    async def update_tag(request):
        id = int(request.match_info['id'])
        exists = TagRepo.fecth_is_exists(session, id)
        if exists == False:
            return Tools.encoderJson(Tools.errorNotFound('Tag'))
        data = await request.json()
        tagEncoded = Tools.encoderJson(data)
        tag = TagRepo.fetch_by_id(session, id)

        url = Tools.getUrl(session, data, tagEncoded, id, TagRepo)
        title = Tools.getTitle(session, data, tagEncoded, id, TagRepo)

        tagFinal = {}
        tag.id = id
        tag.title = title
        tag.url = url
        await TagRepo.update(session, tag_data=tag)
        tagFinal['id'] = id
        tagFinal['title'] = tag.title
        tagFinal['url'] = tag.url
        return Tools.finalResponse(tagFinal)

    async def create_tag(request):
        data = await request.json()
        if 'title' not in data:
            return Tools.finalResponse({'error': '"title" is a required field'})
        title = data['title']
        if not isinstance(title, str) or not len(title):
            return Tools.finalResponse({'error': '"title" must be a string with at least one character'})
        new_id = TagRepo.fetch_get_last_key(session) + 1
        data['url'] = str(request.url.join(request.app.router['one_tag'].url_for(id=str(new_id))))

        await TagRepo.create(session, new_id, title, data['url'])

        return web.Response(
            headers={'Location': data['url']},
            status=303
        )

    async def remove_all_tags(request):
        await Relation.delete_all(session)
        await TagRepo.delete_all(session)
        return web.Response(status=204)

    async def remove_tag(request):
        id = int(request.match_info['id'])
        exists = TagRepo.fecth_is_exists(session, id)
        if exists == False:
            return Tools.finalResponse(Tools.errorNotFound('Tag'))
        await TagRepo.delete(session, id)
        return web.Response(status=204)


class RelationT:
    async def create_relation_tags_by_todo(request):
        id_todo = int(request.match_info['id'])
        data = await request.json()
        id_tag = data['id']
        todo = TodoRepo.fetch_by_id(session, id_todo)
        exists = TodoRepo.fecth_is_exists(session, id_todo)
        exists_tag = TagRepo.fecth_is_exists(session, id_tag)
        if exists == False:
            return Tools.finalResponse(Tools.errorNotFound('Todo'))

        if exists_tag == False:
            return Tools.finalResponse(Tools.errorNotFound('Tag'))

        exists_relation = Relation.fecth_is_exists(session, id_todo, id_tag)
        if exists_relation == True:
            return Tools.finalResponse({'error': 'The association exists'})

        await Relation.create(session, id_todo, id_tag)
        todo = TodoRepo.fetch_by_id(session, id_todo)
        tags = Relation.fetch_all_by_id_todo(session, id_todo)
        todoFinal = jsonable_encoder(todo)
        tagFinal = jsonable_encoder(tags)
        if Tools.isEmpty(tags) == 0:
            todoFinal["tags"] = []
        else:
            todoFinal["tags"] = tagFinal
        return Tools.finalResponse(todoFinal)

    async def create_todo_ans_asociated_tag(request):
        id_todo = int(request.match_info['id'])
        tags = Relation.fetch_all_by_id_todo(session, id_todo)
        tagFinal = jsonable_encoder(tags)
        return Tools.finalResponse(tagFinal)

    async def retrieve_the_todo_list_by_tag(request):
        id_tag = int(request.match_info['id'])
        exists = TagRepo.fecth_is_exists(session, id_tag)
        if exists == False:
            return Tools.finalResponse({Tools.encoderJson('Tag')})

        todos = Relation.fetch_all_by_id_tag(session, id_tag)
        todosFinal = jsonable_encoder(todos)
        if Tools.isEmpty(todos) is True:
            return web.json_response([])
        else:
            return web.json_response(todosFinal)

    async def remove_one_tag_asociation(request):
        id_todo = int(request.match_info['id_t'])
        id_tag = int(request.match_info['id_tg'])
        await  Relation.delete(session, id_todo, id_tag)
        return web.Response(status=204)

    async def remove_all_tag_asociation(request):
        id_todo = int(request.match_info['id'])
        tags = Relation.fetch_all_by_id_todo(session, id_todo)
        tag_f = Tools.encoderJson(tags)
        for tag in tag_f:
            id_tag = tag['id']
            await Relation.delete(session, id_todo, id_tag)
        return web.Response(status=204)
