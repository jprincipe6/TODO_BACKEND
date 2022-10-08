import logging

import aiohttp_cors
from aiohttp import web

import views

PORT = 8080
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

cors.add(app.router.add_get('/todos/', views.Todos.get_all_todos, name='all_todos'))
cors.add(app.router.add_post('/todos/', views.Todos.create_todo, name='create_todo'))
cors.add(app.router.add_get('/todos/{id:\d+}', views.Todos.get_one_todo, name='one_todo'))
cors.add(app.router.add_delete('/todos/', views.Todos.remove_all_todos, name='remove_todos'))
cors.add(app.router.add_patch('/todos/{id:\d+}', views.Todos.update_todo, name='update_todo'))
cors.add(app.router.add_delete('/todos/{id:\d+}', views.Todos.remove_todo, name='remove_todo'))

cors.add(app.router.add_get('/tags/', views.Tags.get_all_tags, name='all_tags'))
cors.add(app.router.add_delete('/tags/', views.Tags.remove_all_tags, name='remove_tags'))
cors.add(app.router.add_post('/tags/', views.Tags.create_tag, name='create_tag'))
cors.add(app.router.add_get('/tags/{id:\d+}', views.Tags.get_one_tag, name='one_tag'))
cors.add(app.router.add_patch('/tags/{id:\d+}', views.Tags.update_tag, name='update_tag'))
cors.add(app.router.add_delete('/tags/{id:\d+}', views.Tags.remove_tag, name='remove_tag'))
#
#
cors.add(
    app.router.add_post('/todos/{id:\d+}/tags/', views.RelationT.create_relation_tags_by_todo,
                        name='create_relation_tags_by_todo'))
cors.add(
    app.router.add_get('/todos/{id:\d+}/tags/', views.RelationT.create_todo_ans_asociated_tag,
                       name='create_todo_ans_asociated_tag'))
cors.add(app.router.add_delete('/todos/{id_t:\d+}/tags/{id_tg:\d+}', views.RelationT.remove_one_tag_asociation,
                               name='remove_one_tag_asociation'))
cors.add(app.router.add_delete('/todos/{id:\d+}/tags/', views.RelationT.remove_all_tag_asociation,
                               name='remove_all_tag_asociation'))

cors.add(
    app.router.add_get('/tags/{id:\d+}/todos/', views.RelationT.retrieve_the_todo_list_by_tag,
                       name='retrieve_the_todo_list_by_tag'))

logging.basicConfig(level=logging.DEBUG)
web.run_app(app, port=PORT)
