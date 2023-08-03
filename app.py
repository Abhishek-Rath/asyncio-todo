import asyncio
from aiohttp import web
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from models import Todo, SessionFactory

# Get todos
async def get_todo(request):
    async with SessionFactory() as session:
        todos = await session.execute(select(Todo))
        todo_list = [{"id": todo.id, "title": todo.title, "completed": todo.completed} for todo in todos.scalars()]
        # print(todo_list)
        return web.json_response(todo_list)

# Post todo
async def create_todo(request):
    data = await request.json()
    async with SessionFactory() as session:
        todo = Todo(title=data['title'])
        session.add(todo)
        await session.commit()
        return web.json_response({
            "message": "Todo Created",
            "id":todo.id,
        })

# Update todo
async def update_todo(request):
    data = await request.json()
    # print(request)
    todo_id = int(request.match_info['todo_id'])

    async with SessionFactory() as session:
        todo = await session.get(Todo, todo_id)
        if not todo:
            return web.json_response({
                'error': "Todo not found!"
            })
        
        todo.title = data.get('title', todo.title)
        todo.completed = data.get('completed', todo.completed)
        await session.commit()
        return web.json_response({
            "message": "Todo updated successfully!"}, status=404)

# Delete todo
async def delete_todo(request):
    todo_id = int(request.match_info['todo_id'])
    async with SessionFactory() as session:
        todo = await session.get(Todo, todo_id)
        if not todo:
            return web.json_response({"message": "Todo doesn't exist!"}, status=404)
        await session.delete(todo)
        await session.commit()
        return web.json_response({
            "message": "Todo deleted successfully!"
        })

async def main():
    app = web.Application()
    app.router.add_post('/todos', create_todo)
    app.router.add_get('/todos', get_todo)
    app.router.add_put('/todos/{todo_id}', update_todo)
    app.router.add_delete('/todos/{todo_id}', delete_todo)
    return app


if __name__ == '__main__':
    # app = asyncio.run(main())
    web.run_app(asyncio.run(main()), host='localhost', port=8080)
