from flask import render_template, request, redirect, current_app
from . import bp
import config
import jwt
import uuid
import aiohttp
from . import doc_file
import math


@bp.route('/', methods=['GET', 'POST'])
async def index():
    if not request.cookies.get('token', False):
        return redirect('/')

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



    if request.method == 'POST':
        id = uuid.uuid4().hex
        title = request.form.get('title')
        party = request.form.get('party')

        doc = request.files.get('doc', '')
        doc = await doc_file.convert(doc)

        needed_credits = math.ceil(len(doc) / 1500)


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
                f'{config.API_URL}/doc/complicated-summary',
                params={
                    'token': config.API_TOKEN
                },
                json={
                    'content': doc
                }
            ) as response:
                res = await response.json()
            if not res.get("res", False):
                current_app.logger.info(res)
                return {"warn":"Problem with complicated summary"}
            complicated_sum = res["res"]

    

            async with session.post(
                f'{config.API_URL}/doc/key-points',
                params={
                    'token': config.API_TOKEN
                },
                json={
                    'content': doc
                }
            ) as response:
                res = await response.json()
            if not res.get("res", False):
                current_app.logger.info(res)
                return {"warn":"Problem with key points"}
            key_points = res["res"]
        
    
            async with session.post(
                f'{config.API_URL}/doc/summary',
                params={
                    'party': party,
                    'token': config.API_TOKEN
                },
                json={
                    'content': doc
                }
            ) as response:
                res = await response.json()
            if not res.get("res", False):
                current_app.logger.info(res)
                return {"warn":"Problem with summary"}
            summary = res["res"]
        
    

            async with session.post(
                f'{config.API_URL}/doc/risks',
                params={
                    'party': party,
                    'token': config.API_TOKEN
                },
                json={
                    'content': doc
                }
            ) as response:
                res = await response.json()
            if not res.get("res", False):
                current_app.logger.info(res)
                return {"warn":"Problem with risks"}
            risks = res["res"]
        
    

            async with session.post(
                f'{config.API_URL}/doc/additional-info',
                params={
                    'party': party,
                    'token': config.API_TOKEN
                },
                json={
                    'content': doc
                }
            ) as response:
                res = await response.json()
            if not res.get("res", False):
                current_app.logger.info(res)
                return {"warn":"Problem with additional info"}
            additional_info = res["res"]
    



        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{config.API_URL}/doc',
                params={
                    'id': id,
                    'title': title,
                    'user_id': user_id,
                    'token': config.API_TOKEN
                }
            ) as response:
                response = await response.json()

        if response.get("id", "Error")=="Error":
            current_app.logger.info(res)
            return {"warn":res.get("description", "Can`t create document")}


        with open(f"cache/docs/{id}.txt", "w") as file:
            file.write(doc)

        with open(f"cache/chats/{id}.txt", "w") as file:
            file.write("")



        with open(f"cache/complicated-summaries/{id}.txt", "w") as file:
            file.write(complicated_sum)

        with open(f"cache/key-points/{id}.txt", "w") as file:
            file.write(key_points)

        with open(f"cache/summaries/{id}.txt", "w") as file:
            file.write(summary)

        with open(f"cache/risks/{id}.txt", "w") as file:
            file.write(risks)

        with open(f"cache/additional-infos/{id}.txt", "w") as file:
            file.write(additional_info)


        return {"id": id}


    return render_template("add-doc.html", credits=credits)




@bp.route('/credits', methods=['POST'])
async def credits_for_file():
    doc = request.files.get('doc', '')
    doc = await doc_file.convert(doc)

    needed_credits = math.ceil(len(doc) / 1500)

    return {"credits": needed_credits}