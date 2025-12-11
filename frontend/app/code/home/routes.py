from flask import render_template, request, redirect, current_app
from . import bp
import config
import aiohttp
import jwt
from . import doc_chat
import os
import math


@bp.route('/', methods=['GET', 'POST'])
async def index():
    if not request.cookies.get('token', False):
        return redirect('/')
    
    token = request.cookies.get('token')

    user_id = jwt.decode(
        token,
        key=config.JWT_SECRET_KEY,
        algorithms=["HS256"],
        options={"verify_sub": False}
    )["sub"]

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{config.API_URL}/doc/user',
            params={
                'user_id': user_id,
                'token': config.API_TOKEN
            }
        ) as response:
            response = await response.json()

    docs = response["docs"]


    # Get user credits
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{config.API_URL}/credits',
            params={
                'id': user_id,
                'token': config.API_TOKEN
            }
        ) as response:
            res = await response.json()
        if not res.get("credits", False):
            current_app.logger.info(res)
            return {"warn":"Problems with getting credits"}
        credits = res["credits"]


    return render_template("home.html", docs = docs, credits=credits)


@bp.route('/<string:id>/chat', methods=['GET'])
async def get_chat(id):
    with open(f"cache/chats/{id}.txt", "r") as file:
        chat = await doc_chat.json_convert(file.read())

    return {"chat": chat}


@bp.route('/<string:id>', methods=['GET', 'POST, DELETE'])
async def home_doc(id: str):
    if not request.cookies.get('token', False):
        return redirect('/')
    
    if request.method == 'DELETE':
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f'{config.API_URL}/doc',
                params={
                    'id': id,
                    'token': config.API_TOKEN
                }
            ) as response:
                response = await response.json()
                print(response)

        return redirect('/home')


    
    token = request.cookies.get('token')

    user_id = jwt.decode(
        token,
        key=config.JWT_SECRET_KEY,
        algorithms=["HS256"],
        options={"verify_sub": False}
    )["sub"]

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{config.API_URL}/doc/user',
            params={
                'user_id': user_id,
                'token': config.API_TOKEN
            }
        ) as response:
            response = await response.json()

    docs = response["docs"]
    title = next((doc_el["title"] for doc_el in docs if doc_el["id"]==id), None)


    # Get user credits
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{config.API_URL}/credits',
            params={
                'id': user_id,
                'token': config.API_TOKEN
            }
        ) as response:
            res = await response.json()
        if not res.get("credits", False):
            current_app.logger.info(res)
            return {"warn":"Problems with getting credits"}
        credits = res["credits"]

    
    # Get cache files
    with open(f"cache/docs/{id}.txt", "r") as file:
        doc = file.read().replace('\n', '<br>')
        sum_doc_chars = len(file.read())
    
    with open(f"cache/summaries/{id}.txt", "r") as file:
        doc_summary = file.read().replace('\n', '<br>')
    
    with open(f"cache/key-points/{id}.txt", "r") as file:
        doc_key_points = file.read().replace('\n', '<br>')
    
    with open(f"cache/risks/{id}.txt", "r") as file:
        doc_risk = file.read().replace('\n', '<br>')
    
    with open(f"cache/additional-infos/{id}.txt", "r") as file:
        doc_additional_info = file.read().replace('\n', '<br>')


    with open(f"cache/complicated-summaries/{id}.txt", "r") as file:
        sum_chars = len(file.read())


    return render_template(
        "home.html",
        docs = docs,
        doc_id = id,
        doc = doc,
        doc_title = title,
        doc_summary = doc_summary,
        doc_key_points = doc_key_points,
        doc_risk = doc_risk,
        doc_additional_info = doc_additional_info,
        credits = credits,
        sum_doc_chars = sum_doc_chars,
        sum_chars = sum_chars
    )


@bp.route('/<string:id>/delete', methods=['POST'])
async def delete_doc(id: str):
    if not request.cookies.get('token', False):
        return redirect('/')
    
    async with aiohttp.ClientSession() as session:
        async with session.delete(
            f'{config.API_URL}/doc',
            params={
                'id': id,
                'token': config.API_TOKEN
            }
        ) as response:
            response = await response.json()
            print(response)
    
    if os.path.exists(f"cache/docs/{id}.txt"):
        os.remove(f"cache/docs/{id}.txt")

    if os.path.exists(f"cache/chats/{id}.txt"):
        os.remove(f"cache/chats/{id}.txt")
    
    if os.path.exists(f"cache/complicated-summaries/{id}.txt"):
        os.remove(f"cache/complicated-summaries/{id}.txt")
    
    if os.path.exists(f"cache/summaries/{id}.txt"):
        os.remove(f"cache/summaries/{id}.txt")
    
    if os.path.exists(f"cache/key-points/{id}.txt"):
        os.remove(f"cache/key-points/{id}.txt")
    
    if os.path.exists(f"cache/risks/{id}.txt"):
        os.remove(f"cache/risks/{id}.txt")
    
    if os.path.exists(f"cache/additional-infos/{id}.txt"):
        os.remove(f"cache/additional-infos/{id}.txt")

    return redirect('/home')



@bp.route('/<string:id>/explain-part', methods=['POST'])
async def explain_part(id: str):
    if not request.cookies.get('token', False):
        return redirect('/')
    
    with open(f"cache/docs/{id}.txt", "r") as file:
        content = file.read()

    
    content_part = request.form.get('content')
    needed_credits = math.ceil((len(content_part)+len(content))/6000)
    
    with open(f"cache/chats/{id}.txt", "a") as file:
        file.write(f'\n----User----\nExplain me please this text\n\n{content_part}')
    



    # Get user id
    token = request.cookies.get('token')
    user_id = jwt.decode(
        token,
        key=config.JWT_SECRET_KEY,
        algorithms=["HS256"],
        options={"verify_sub": False}
    )["sub"]


    # Get user credits
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{config.API_URL}/credits',
            params={
                'id': user_id,
                'token': config.API_TOKEN
            }
        ) as response:
            res = await response.json()
    if not res.get("credits", False):
        current_app.logger.info(res)
        return {"warn":"Problem with getting credits"}
    credits = res["credits"]

    if credits < needed_credits:
        return {"warn":"Not enough credits"}



    async with aiohttp.ClientSession() as session:
        async with session.patch(
            f'{config.API_URL}/credits',
            params={
                'id': user_id,
                'credits': needed_credits,
                'token': config.API_TOKEN
            }
        ) as response:
            res = await response.json()
    if not res.get("credits", False):
        current_app.logger.info(res)
        return {"warn":"Can`t minus credits"}


    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'{config.API_URL}/doc/explain-part',
            params={
                'token': config.API_TOKEN
            },
            json={
                "content": content,
                "content_part": content_part
            }
        ) as response:
            res = await response.json()
    
    if not res.get("res", False):
        current_app.logger.info(res)
        return {"warn":"Problem with explain part"}
    

    with open(f"cache/chats/{id}.txt", "a") as file:
        file.write(f'\n----AI----\n{res["res"]}')


    return {"credits": credits-needed_credits}



@bp.route('/<string:id>/ask/<string:question>', methods=['POST'])
async def ask(id: str, question: str):
    if not request.cookies.get('token', False):
        return redirect('/')
       
    with open(f"cache/complicated-summaries/{id}.txt", "r") as file:
        content = file.read()
        
    with open(f"cache/chats/{id}.txt", "a") as file:
        file.write(f'\n----User----\n{question}')

    needed_credits = math.ceil((len(content)+len(question))/6000)
    

    # Get user id
    token = request.cookies.get('token')
    user_id = jwt.decode(
        token,
        key=config.JWT_SECRET_KEY,
        algorithms=["HS256"],
        options={"verify_sub": False}
    )["sub"]


    # Get user credits
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{config.API_URL}/credits',
            params={
                'id': user_id,
                'token': config.API_TOKEN
            }
        ) as response:
            res = await response.json()
    if not res.get("credits", False):
        current_app.logger.info(res)
        return {"warn":"Problem with getting credits"}
    credits = res["credits"]

    if credits < needed_credits:
        return {"warn":"Not enough credits"}

    

    async with aiohttp.ClientSession() as session:
        async with session.patch(
            f'{config.API_URL}/credits',
            params={
                'id': user_id,
                'credits': needed_credits,
                'token': config.API_TOKEN
            }
        ) as response:
            res = await response.json()
    if not res.get("credits", False):
        current_app.logger.info(res)
        return {"warn":"Can`t minus credits"}
    

    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'{config.API_URL}/doc/ask',
            params={
                'token': config.API_TOKEN,
                'question': question
            },
            json={
                "content": content
            }
        ) as response:
            response = await response.json()
        if not res.get("res", False):
            current_app.logger.info(res)
            return {"warn":"Problem with answer question"}
    
    
    with open(f"cache/chats/{id}.txt", "a") as file:
        file.write(f'\n----AI----\n{response["res"]}')

    return {"credits": credits-needed_credits}