from flask import render_template, request, make_response, redirect
from . import bp
import config
import aiohttp


@bp.route('/', methods=['GET', 'POST'])
async def index():
    if request.cookies.get('token'):
        return redirect('/home')
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{config.API_URL}/auth',
                params={
                    'email': email,
                    'password': password,
                    'token': config.API_TOKEN
                }
            ) as response:
                response = await response.json()
                print(response)

        if not response.get("token", False):
            return render_template("sign-up.html", warn=response["detail"], email=email, password=password)
        

        res = make_response(redirect('/home')) 
        res.set_cookie('token', response["token"]) 

        return res
    
    return render_template("sign-up.html")