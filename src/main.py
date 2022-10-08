import logging

import aiohttp_cors
from aiohttp import web
from fastapi.encoders import jsonable_encoder

import models as models
from db import engine, session
from repositories import TodoRepo, TagRepo, Relation

def get_all_todos(request):
    todo_f = TodoRepo.fetch_all(session)
    if len(todo_f) == 0:
        return web.json_response([])
    else:
        final = []
        for i in range(len(todo_f)):
            todo_d = jsonable_encoder(todo_f[i])
            tags = Relation.fetch_all_by_id_todo(session, todo_d['id'])
            tag_f = jsonable_encoder(tags)
            if len(tag_f) == 0:
                # print("TAG-VACIO")
                # todo_d["tags"]=''
                final.append(jsonable_encoder(todo_d))
            else:
                print("TAG-NO-VACIO")
                todo_d["tags"] = tag_f
                final.append(jsonable_encoder(todo_d))
        return web.json_response(final)


def get_all_tags(request):
    tg = TagRepo.fetch_all(session)
    if len(tg) == 0:
        return web.json_response([])
    else:
        tags = jsonable_encoder(tg)
        print("Tags con todos")
        final = []
        for tag in tags:
            print("TAG_GET")
            print(tag)
            todos = Relation.fetch_all_by_id_tag(session, tag['id'])
            todos_f = jsonable_encoder(todos)
            if (len(todos)) == 0:
                tag['todos'] = []
                final.append(tag)
            else:
                tag['todos'] = todos_f
                print('FINAL: ', tag)
                final.append(tag)
    return web.json_response(final)


def get_one_todo(request):
    id = request.match_info['id']
    todo = TodoRepo.fetch_by_id(session, id)
    exists = TodoRepo.fecth_is_exists(session, id)
    if exists == False:
        return web.json_response({'error': 'Todo not found'}, status=404)

    tags = Relation.fetch_all_by_id_todo(session, id)
    final = []
    todo_f = jsonable_encoder(todo)
    tag_f = jsonable_encoder(tags)
    if len(tags) == 0:
        todo_f["tags"] = []
        final.append(todo_f)
    else:
        todo_f["tags"] = tag_f
        final.append(todo_f)
    return web.json_response(todo_f)


def get_one_tag(request):
    id = request.match_info['id']
    tag = TagRepo.fetch_by_id(session, id)
    exists = TagRepo.fecth_is_exists(session, id)
    if exists == False:
        return web.json_response({'error': 'Todo not found'}, status=404)

    todos = Relation.fetch_all_by_id_tag(session, id)
    todos_f = jsonable_encoder(todos)
    tag_f = jsonable_encoder(tag)
    # final={}
    if (len(todos)) == 0:
        tag_f['todos'] = []
        # final.append(tag_f)
    else:
        tag['todos'] = todos_f
        # print('FINAL: ', tag)
        # final.append(tag)

    # json_compatible_item_data = jsonable_encoder(tag)
    return web.json_response(tag_f)


async def update_todo(request):
    id = int(request.match_info['id'])

    exists = TodoRepo.fecth_is_exists(session, id)
    if exists == False:
        return web.json_response({'error': 'Todo not found'})
    data = await request.json()
    # print(data)
    update_todo_encoded = jsonable_encoder(data)
    completed = None
    if 'completed' not in data:
        completed = TodoRepo.fetch_get_completed(session, id)
    else:
        completed = update_todo_encoded['completed']

    order = None
    if 'order' not in data:
        order = TodoRepo.fetch_get_order(session, id)
    else:
        order = update_todo_encoded['order']

    url = None
    if 'url' not in data:
        url = TodoRepo.fetch_get_url(session, id)
    else:
        url = update_todo_encoded['url']

    title = None
    if 'title' not in data:
        title = TodoRepo.fetch_get_title(session, id)
    else:
        title = update_todo_encoded['title']

    # db_todo = models.Todos(id, title, completed, order, url)
    db_todo = TodoRepo.fetch_by_id(session, id)
    # print(db_todo)
    d = {}
    if db_todo:
        db_todo.id = id
        db_todo.title = title
        db_todo.completed = completed
        db_todo.order = order
        db_todo.url = url
        todo = await TodoRepo.update(session, todo_data=db_todo)
        # json_compatible_item_data = jsonable_encoder(db_todo)
        # print("H",type(todo))
        # print(todo)
    d['id'] = id
    d['title'] = db_todo.title
    d['completed'] = db_todo.completed
    d['order'] = db_todo.order
    d['url'] = db_todo.url
    return web.json_response(d)


async def update_tag(request):
    id = int(request.match_info['id'])
    exists = TagRepo.fecth_is_exists(session, id)
    if exists == False:
        return web.json_response({'error': 'Todo not found'})
    data = await request.json()
    update_tag_encoded = jsonable_encoder(data)

    db_tag = TagRepo.fetch_by_id(session, id)
    title = None
    if 'title' not in data:
        title = TagRepo.fetch_get_title(session, id)
    else:
        title = update_tag_encoded['title']
    url = None
    if 'url' not in data:
        url = TagRepo.fetch_get_url(session, id)
    else:
        url = update_tag_encoded['url']

    d = {}
    if db_tag:
        db_tag.id = id
        db_tag.title = title
        db_tag.url = url
        todo = await TagRepo.update(session, tag_data=db_tag)
        # json_compatible_item_data = jsonable_encoder(db_todo)
        # print("H",type(todo))
        # print(todo)
    d['id'] = id
    d['title'] = db_tag.title
    d['url'] = db_tag.url
    return web.json_response(d)


async def create_todo(request):
    data = await request.json()

    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})
    title = data['title']
    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    data['completed'] = bool(data.get('completed', False))

    new_id = TodoRepo.fetch_get_last_key(session) + 1

    data['url'] = str(request.url.join(request.app.router['one_todo'].url_for(id=str(new_id))))
    order = None
    if 'order' not in data:
        order = None
    else:
        order = data['order']

    await TodoRepo.create(session, new_id, title, data['completed'], order, data['url'])

    return web.json_response(
        headers={'Location': data['url']},
        status=303
    )


async def create_tag(request):
    data = await request.json()
    if 'title' not in data:
        return web.json_response({'error': '"title" is a required field'})
    title = data['title']
    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})
    new_id = TagRepo.fetch_get_last_key(session) + 1
    data['url'] = str(request.url.join(request.app.router['one_tag'].url_for(id=str(new_id))))

    await TagRepo.create(session, new_id, title, data['url'])

    return web.json_response(
        headers={'Location': data['url']},
        status=303
    )


async def create_relation_tags_by_todo(request):
    # print("ESTIY AQUI")
    # id =
    # print(id)
    id_todo = int(request.match_info['id'])
    data = await request.json()
    id_tag = data['id']
    print(data['id'])
    todo = TodoRepo.fetch_by_id(session, id_todo)
    exists = TodoRepo.fecth_is_exists(session, id_todo)
    exists_tag = TagRepo.fecth_is_exists(session, id_tag)
    if exists == False:
        return web.json_response({'error': 'Todo not found'})

    if exists_tag == False:
        return web.json_response({'error': 'Tag not found'})

    exists_relation = Relation.fecth_is_exists(session, id_todo, id_tag)
    if exists_relation == True:
        return web.json_response({'error': 'The association exists'})

    relation = await Relation.create(session, id_todo, id_tag)
    # print(relation.__repr__())
    todo = TodoRepo.fetch_by_id(session, id_todo)
    tags = Relation.fetch_all_by_id_todo(session, id_todo)

    final = []
    todo_f = jsonable_encoder(todo)
    tag_f = jsonable_encoder(tags)
    # tag_f[0]['title']='joined tag'
    # todo_f["tags"] = tag_f
    # final.append(todo_f)
    print(todo_f)
    if len(tags) == 0:
        todo_f["tags"] = []
        final.append(todo_f)
    else:
        todo_f["tags"] = tag_f
        final.append(todo_f)
    return web.json_response(todo_f)


async def create_todo_ans_asociated_tag(request):
    id_todo = int(request.match_info['id'])
    # todo = TodoRepo.fetch_by_id(session, id_todo)

    tags = Relation.fetch_all_by_id_todo(session, id_todo)
    tag_f = jsonable_encoder(tags)
    return web.json_response(tag_f)


def retrieve_the_todo_list_by_tag(request):
    print('retrieve_the_todo_list_by_tag')
    id_tag = int(request.match_info['id'])
    exists = TagRepo.fecth_is_exists(session, id_tag)
    if exists == False:
        return web.json_response({'error': 'Tag not found'})

    todos = Relation.fetch_all_by_id_tag(session, id_tag)
    todos_f = jsonable_encoder(todos)
    print(todos_f)
    if (len(todos) == 0):
        return web.json_response([])
    else:
        return web.json_response(todos_f)


async def remove_all_todos(request):
    await Relation.delete_all(session)
    # await TagRepo.delete_all(session)
    await TodoRepo.delete_all(session)

    return web.Response(status=204)


async def remove_all_tags(request):
    await Relation.delete_all(session)
    await TagRepo.delete_all(session)
    return web.Response(status=204)


async def remove_one_tag_asociation(request):
    id_todo = int(request.match_info['id_t'])
    id_tag = int(request.match_info['id_tg'])
    await  Relation.delete(session, id_todo, id_tag)
    return web.Response(status=204)


async def remove_all_tag_asociation(request):
    id_todo = int(request.match_info['id'])
    tags = Relation.fetch_all_by_id_todo(session, id_todo)
    tag_f = jsonable_encoder(tags)
    for tag in tag_f:
        id_tag = tag['id']
        await Relation.delete(session, id_todo, id_tag)
    return web.Response(status=204)


async def remove_todo(request):
    id = int(request.match_info['id'])

    exists = TodoRepo.fecth_is_exists(session, id)
    if exists == False:
        # return web.json_response({'error': 'Todo not found'}, status=404)
        return web.json_response({'error': 'Todo not found'})

    await TodoRepo.delete(session, id)

    return web.Response(status=204)


async def remove_tag(request):
    id = int(request.match_info['id'])

    exists = TagRepo.fecth_is_exists(session, id)
    if exists == False:
        # return web.json_response({'error': 'Todo not found'}, status=404)
        return web.json_response({'error': 'Todo not found'})
    await TagRepo.delete(session, id)

    return web.Response(status=204)


app = web.Application()

# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*",
        allow_methods="*",
    )
})

cors.add(app.router.add_get('/todos/', get_all_todos, name='all_todos'))
cors.add(app.router.add_post('/todos/', create_todo, name='create_todo'))
cors.add(app.router.add_get('/todos/{id:\d+}', get_one_todo, name='one_todo'))
cors.add(app.router.add_delete('/todos/', remove_all_todos, name='remove_todos'))
cors.add(app.router.add_patch('/todos/{id:\d+}', update_todo, name='update_todo'))
cors.add(app.router.add_delete('/todos/{id:\d+}', remove_todo, name='remove_todo'))

cors.add(app.router.add_get('/tags/', get_all_tags, name='all_tags'))
cors.add(app.router.add_delete('/tags/', remove_all_tags, name='remove_tags'))
cors.add(app.router.add_post('/tags/', create_tag, name='create_tag'))
cors.add(app.router.add_get('/tags/{id:\d+}', get_one_tag, name='one_tag'))
cors.add(app.router.add_patch('/tags/{id:\d+}', update_tag, name='update_tag'))
cors.add(app.router.add_delete('/tags/{id:\d+}', remove_tag, name='remove_tag'))
#
#
cors.add(
    app.router.add_post('/todos/{id:\d+}/tags/', create_relation_tags_by_todo, name='create_relation_tags_by_todo'))
cors.add(
    app.router.add_get('/todos/{id:\d+}/tags/', create_todo_ans_asociated_tag, name='create_todo_ans_asociated_tag'))
cors.add(app.router.add_delete('/todos/{id_t:\d+}/tags/{id_tg:\d+}', remove_one_tag_asociation,
                               name='remove_one_tag_asociation'))
cors.add(app.router.add_delete('/todos/{id:\d+}/tags/', remove_all_tag_asociation, name='remove_all_tag_asociation'))

cors.add(
    app.router.add_get('/tags/{id:\d+}/todos/', retrieve_the_todo_list_by_tag, name='retrieve_the_todo_list_by_tag'))

logging.basicConfig(level=logging.DEBUG)
web.run_app(app, port=8080)
