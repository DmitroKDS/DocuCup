from flask import render_template, request, redirect
from . import bp

@bp.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == "POST":
        if request.cookies.get('token'):
            return redirect('/home')
        return redirect('/sign-up')
    
    return render_template("main.html", auth=request.cookies.get('token', False))