from flask import render_template, request, redirect, make_response
import config
from . import bp
import aiohttp

@bp.route('/', methods=['GET', 'POST'])
async def index():
    if request.cookies.get('token'):
        return redirect('/home')
    
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{config.API_URL}/auth',
                params={
                    'email': email,
                    'password': password,
                    'token': config.API_TOKEN
                }
            ) as response:
                response = await response.json()

        if not response.get("token", False):
            return render_template("log-in.html", warn=response["detail"], email=email, password=password)
        

        res = make_response(redirect('/home')) 
        res.set_cookie('token', response["token"]) 

        return res
    
    return render_template("log-in.html")