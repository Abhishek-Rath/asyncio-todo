import asyncio
from aiohttp import web
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from models import Todo, SessionFactory


async def get_todo(request):
    async with SessionFactory() as session:
        todos = await session.execute(select(Todo))
        todo_list = [{"id": todo.id, "title": todo.title, "completed": todo.completed} for todo in todos.scalars()]
        print(todo_list)
        return web.json_response(todo_list)

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

async def main():
    app = web.Application()
    app.router.add_post('/todos', create_todo)
    app.router.add_get('/todos', get_todo)
    return app


if __name__ == '__main__':
    # app = asyncio.run(main())
    web.run_app(asyncio.run(main()), host='localhost', port=8080)
