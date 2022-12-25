from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Newsblock, Source, User
from django.contrib.sessions.models import Session
import urllib.request
import requests

# Create your views here.

def detail(request, article_id):
    article_paragraphs = ''
    new = ''
    if Newsblock.objects.filter(id=article_id):
        new = Newsblock.objects.filter(id=article_id)[0]
        article_paragraphs = new.text.split('/n')

    user_name = 'Войти'
    if not request.session.is_empty():
        if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
            user_name = request.session["user_name"]
            user_login = request.session["user_login"]
            user_password = request.session["user_password"]
            if not User.objects.filter(user_name=user_name, user_login=user_login,
                                       user_password=user_password).exists():
                user_name = 'Войти'

    return render(request, 'main/article.html',
                  {'user_name': user_name, 'recovered_day': '450510', 'recovered': '425', 'cases': '490',
                   'cases_day': '530912', 'article': new, 'article_paragraphs': article_paragraphs, 'bitcoin_price': '45950',
                   'gbp_price': '112.64', 'usd_price': '94.71', 'eur_price': '85.75'})

def article(request):
    id = request.GET.get('id', '')
    link = request.GET.get('next', '')
    if link == "/article":
        if not request.session.is_empty():
            if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
                user_name = request.session["user_name"]
                user_login = request.session["user_login"]
                user_password = request.session["user_password"]
                # Пользователь авторизован
                if User.objects.filter(user_name=user_name, user_login=user_login, user_password=user_password).exists():
                    user = User.objects.get(user_name=user_name, user_login=user_login, user_password=user_password)
                    viewed_news = user.viewed_news.all()
                    if Newsblock.objects.get(id=id) not in viewed_news:
                        user.viewed_news.add(Newsblock.objects.get(id=id))
                    new = Newsblock.objects.get(id=id)
        link += '/' + id
        HttpResponseRedirect(link)

    elif id != '' and link != '':
        if not request.session.is_empty():
            if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
                user_name = request.session["user_name"]
                user_login = request.session["user_login"]
                user_password = request.session["user_password"]
                if not User.objects.filter(user_name=user_name, user_login=user_login,
                                           user_password=user_password).exists():
                    return HttpResponseRedirect(link)
                else:  # Пользователь авторизован (инкремент)
                    user = User.objects.get(user_name=user_name, user_login=user_login, user_password=user_password)
                    viewed_news = user.viewed_news.all()
                    if Newsblock.objects.get(id=id) not in viewed_news:
                        user.viewed_news.add(Newsblock.objects.get(id=id))
                    new = Newsblock.objects.get(id=id)
                    new.views_count += 1
                    new.save()
                    return HttpResponseRedirect(link)
            else:
                return HttpResponseRedirect(link)
        else:
            return HttpResponseRedirect(link)

    # news = Newsblock.objects.all().order_by('?')

    user_name = 'Войти'

    if not request.session.is_empty():
        if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
            user_name = request.session["user_name"]
            user_login = request.session["user_login"]
            user_password = request.session["user_password"]
            if not User.objects.filter(user_name=user_name, user_login=user_login,
                                       user_password=user_password).exists():
                user_name = 'Войти'

    url = '/article'
    return render(request, 'main/article.html',
                  {'url': url, 'user_name': user_name, 'recovered_day': '450510', 'recovered': '425', 'cases': '490',
                   'cases_day': '530912', 'article': new, 'bitcoin_price': '45950',
                   'gbp_price': '112.64', 'usd_price': '94.71', 'eur_price': '85.75'})


def authorization(request):
    if request.method == 'POST':
        login = request.POST['login']
        password = request.POST['password']
        error_password_message = ''
        error_login_message = ''
        if User.objects.filter(user_login=login).exists():
            if User.objects.filter(user_login=login, user_password=password).exists():
                user = User.objects.get(user_login=login, user_password=password)
                request.session["user_name"] = user.user_name
                request.session["user_login"] = user.user_login
                request.session["user_password"] = user.user_password
                return HttpResponseRedirect('/profile/')
            else:
                error_password_message = 'Неправильный пароль'
        else:
            error_login_message = 'Такого пользователя не существует'
        return render(request, 'main/authorization.html', {'error_login_message': error_login_message, 'error_password_message': error_password_message})

    if not request.session.is_empty():
        if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
            user_name = request.session["user_name"]
            user_login = request.session["user_login"]
            user_password = request.session["user_password"]
            if User.objects.filter(user_name=user_name, user_login=user_login, user_password=user_password).exists():
                return HttpResponseRedirect('/profile/')
    return render(request, 'main/authorization.html')

def registration(request):
    if request.method == 'POST':
        user = request.POST['user']
        login = request.POST['login']
        password = request.POST['password']
        if len(user) > 40 or len(user) < 3 or len(login) > 20 or len(login) < 3 or len(password) > 30 or len(password) < 3 or User.objects.filter(user_login=login).exists():
            error_user_message = ''
            error_login_message = ''
            error_password_message = ''
            if len(user) > 40:
                error_user_message = 'Слишком много символов!'
            if len(user) < 3:
                error_user_message = 'Слишком мало символов!'
            if len(login) > 40:
                error_login_message = 'Слишком много символов!'
            if len(login) < 3:
                error_login_message = 'Слишком мало символов!'
            if User.objects.filter(user_login=login).exists():
                error_login_message = 'Номер телефона уже используется'
            if len(password) > 40:
                error_password_message = 'Слишком много символов!'
            if len(password) < 3:
                error_password_message = 'Слишком мало символов!'
            return render(request, 'main/registration.html', {'error_user_message': error_user_message, 'error_login_message': error_login_message, 'error_password_message': error_password_message})
        else:
            u = User(user_name=user, user_login=login, user_password=password)
            u.save()
            # Тут сессия
            request.session['user_name'] = user
            request.session['user_login'] = login
            request.session['user_password'] = password
            return HttpResponseRedirect('/profile/')
    else:
        return render(request, 'main/registration.html')

def profile(request):

    if request.session.is_empty():
        return HttpResponseRedirect('/main/')
    sources = Source.objects.all()
    user = User.objects.filter(user_login=request.session['user_login'])[0]
    followed_sources = user.followed_sources.all().filter(user=user.id)
    ids = []
    for f in followed_sources:
        ids.append(f.source_id)

    # Проверка просмотр ли это новости
    id = request.GET.get('id', '')
    link = request.GET.get('next', '')


    if link == "/article":
        if not request.session.is_empty():
            if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
                user_name = request.session["user_name"]
                user_login = request.session["user_login"]
                user_password = request.session["user_password"]
                # Пользователь авторизован
                if User.objects.filter(user_name=user_name, user_login=user_login, user_password=user_password).exists():
                    user = User.objects.get(user_name=user_name, user_login=user_login, user_password=user_password)
                    viewed_news = user.viewed_news.all()
                    if Newsblock.objects.get(id=id) not in viewed_news:
                        user.viewed_news.add(Newsblock.objects.get(id=id))
                    new = Newsblock.objects.get(id=id)
        link += '/' + id
        HttpResponseRedirect(link)



    if id != '' and link != '':
        if not request.session.is_empty():
            if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
                user_name = request.session["user_name"]
                user_login = request.session["user_login"]
                user_password = request.session["user_password"]
                if not User.objects.filter(user_name=user_name, user_login=user_login,
                                           user_password=user_password).exists():
                    return HttpResponseRedirect(link)
                else:  # Пользователь авторизоован (инкремент)
                    user = User.objects.get(user_name=user_name, user_login=user_login, user_password=user_password)
                    viewed_news = user.viewed_news.all()
                    if Newsblock.objects.get(id=id) not in viewed_news:
                        user.viewed_news.add(Newsblock.objects.get(id=id))
                    new = Newsblock.objects.get(id=id)
                    return HttpResponseRedirect(link)
            else:
                return HttpResponseRedirect(link)
        else:
            return HttpResponseRedirect(link)

    # news - последние по подпискам

    q = [Newsblock.objects.all().order_by('-id')]

    for i in range(0, 5):
        if i+1 not in ids:
            q.append(q[i].exclude(source_id=i+1))
        else:
            q.append(q[i])
    news = q[5][:20]

    # viewed_news - просмотренные новости

    viewed_news = user.viewed_news.all().filter(user=user.id).order_by('-id')
    url = '/profile/'

    return render(request, 'main/profile.html', {'url': url, 'viewed_news': viewed_news, 'news': news, 'followed_sources': ids, 'user': user, 'sources': sources})

def leave(request):
    request.session['user_login'] = None
    request.session['user_name'] = None
    request.session['user_password'] = None
    return HttpResponseRedirect('/main/')

def changesubs(request):
    if request.session.is_empty():
        return HttpResponseRedirect('/main/')
    tass = request.POST.get('tass', False)
    iz = request.POST.get('iz', False)
    lenta = request.POST.get('lenta', False)
    ixbt = request.POST.get('ixbt', False)
    match = request.POST.get('match', False)
    telegram = request.POST.get('telegram', False)
    user = User.objects.filter(user_login=request.session['user_login'])[0]
    followed_sources = user.followed_sources.all().filter(user=user.id)
    ids = []
    sources = [tass, iz, lenta, ixbt, match]

    # Редактирование уже созданных элементов бд
    for f in followed_sources:
        ids.append(f.source_id)
    i = 0
    for s in sources:
        i += 1
        if s and i not in ids:
            user.followed_sources.add(Source.objects.get(source_id=i))
        elif not s and i in ids:
            user.followed_sources.remove(Source.objects.get(source_id=i))
    if telegram == "on":
        telegram = True
    if telegram != user.telegram_notification:
        user.telegram_notification=telegram
        user.save()

    return HttpResponseRedirect('/profile/')

def index(request):

    id = request.GET.get('id', '')
    link = request.GET.get('next', '')


    if link == "/article":
        if not request.session.is_empty():
            if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
                user_name = request.session["user_name"]
                user_login = request.session["user_login"]
                user_password = request.session["user_password"]
                # Пользователь авторизован
                if User.objects.filter(user_name=user_name, user_login=user_login, user_password=user_password).exists():
                    user = User.objects.get(user_name=user_name, user_login=user_login, user_password=user_password)
                    viewed_news = user.viewed_news.all()
                    if Newsblock.objects.get(id=id) not in viewed_news:
                        user.viewed_news.add(Newsblock.objects.get(id=id))
                    new = Newsblock.objects.get(id=id)
        link += '/' + id
        HttpResponseRedirect(link)



    print(link)
    if id != '' and link != '':
        if not request.session.is_empty():
            if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
                user_name = request.session["user_name"]
                user_login = request.session["user_login"]
                user_password = request.session["user_password"]
                if not User.objects.filter(user_name=user_name, user_login=user_login, user_password=user_password).exists():
                    return HttpResponseRedirect(link)
                else:  # Пользователь авторизоован (инкремент)
                    user = User.objects.get(user_name=user_name, user_login=user_login, user_password=user_password)
                    viewed_news = user.viewed_news.all()
                    if Newsblock.objects.get(id=id) not in viewed_news:
                        user.viewed_news.add(Newsblock.objects.get(id=id))
                    new = Newsblock.objects.get(id=id)
                    new.views_count += 1
                    new.save()
                    return HttpResponseRedirect(link)
            else:
                return HttpResponseRedirect(link)
        else:
            return HttpResponseRedirect(link)

    sources = Source.objects.all()

    news = Newsblock.objects.all().order_by('?')

    user_name = 'Войти'

    if not request.session.is_empty():
        if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
            user_name = request.session["user_name"]
            user_login = request.session["user_login"]
            user_password = request.session["user_password"]
            if not User.objects.filter(user_name=user_name, user_login=user_login, user_password=user_password).exists():
                user_name = 'Войти'

    url = '/main/'
    return render(request, 'main/news.html', {'url': url, 'user_name': user_name, 'recovered_day': '450510', 'recovered': '425','cases': '490', 'cases_day': '530912', 'news': news, 'bitcoin_price': '45950', 'sources': sources, 'gbp_price': '112.64', 'usd_price': '94.71', 'eur_price': '85.75'})

def news(request):
    id = request.GET.get('id', '')
    link = request.GET.get('next', '')


    if link == "/article":
        if not request.session.is_empty():
            if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
                user_name = request.session["user_name"]
                user_login = request.session["user_login"]
                user_password = request.session["user_password"]
                # Пользователь авторизован
                if User.objects.filter(user_name=user_name, user_login=user_login, user_password=user_password).exists():
                    user = User.objects.get(user_name=user_name, user_login=user_login, user_password=user_password)
                    viewed_news = user.viewed_news.all()
                    if Newsblock.objects.get(id=id) not in viewed_news:
                        user.viewed_news.add(Newsblock.objects.get(id=id))
                    new = Newsblock.objects.get(id=id)
        link += '/' + id
        HttpResponseRedirect(link)



    print(link)
    if id != '' and link != '':
        if not request.session.is_empty():
            if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
                user_name = request.session["user_name"]
                user_login = request.session["user_login"]
                user_password = request.session["user_password"]
                if not User.objects.filter(user_name=user_name, user_login=user_login,
                                           user_password=user_password).exists():
                    return HttpResponseRedirect(link)
                else:  # Пользователь авторизоован (инкремент)
                    user = User.objects.get(user_name=user_name, user_login=user_login, user_password=user_password)
                    viewed_news = user.viewed_news.all()
                    if Newsblock.objects.get(id=id) not in viewed_news:
                        user.viewed_news.add(Newsblock.objects.get(id=id))
                    new = Newsblock.objects.get(id=id)
                    new.views_count += 1
                    new.save()
                    return HttpResponseRedirect(link)
            else:
                return HttpResponseRedirect(link)
        else:
            return HttpResponseRedirect(link)

    sources = Source.objects.all()


    tass = request.POST.get('tass', False)
    iz = request.POST.get('iz', False)
    lenta = request.POST.get('lenta', False)
    ixbt = request.POST.get('ixbt', False)
    match = request.POST.get('match', False)
    key_word = request.POST['key_word']

    q = Newsblock.objects.all()

    if tass == False:
        q1 = q.exclude(source_id=1)
    else:
        q1 = q

    if iz == False:
        q2 = q1.exclude(source_id=2)
    else:
        q2 = q1

    if lenta == False:
        q3 = q2.exclude(source_id=3)
    else:
        q3 = q2

    if ixbt == False:
        q4 = q3.exclude(source_id=4)
    else:
        q4 = q3

    if match == False:
        q5 = q4.exclude(source_id=5)
    else:
        q5 = q4

    news = q5

    if key_word != "":
        m = news.filter(title__icontains=key_word).order_by('?')
    else:
        m = news.order_by('?')

    if len(m) < 10:
        dop = Newsblock.objects.all().order_by('?')[:15]
    else:
        dop = False

    user_name = 'Войти'
    if not request.session.is_empty():
        if request.session["user_name"] and request.session["user_login"] and request.session["user_password"]:
            user_name = request.session["user_name"]
            user_login = request.session["user_login"]
            user_password = request.session["user_password"]
            if not User.objects.filter(user_name=user_name, user_login=user_login, user_password=user_password).exists():
                user_name = 'Войти'

    url = '/news/'
    return render(request, 'main/sortednews.html', {'url': url, 'user_name': user_name, 'recovered_day': '450510', 'recovered': '425','cases': '490', 'cases_day': '530912', 'dop': dop,'news': m, 'bitcoin_price': '45950', 'sources': sources, 'gbp_price': '112.64', 'usd_price': '94.71', 'eur_price': '85.75'})
