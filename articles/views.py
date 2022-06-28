from django.shortcuts import render, HttpResponse, redirect
from .models import Article
import requests
import re
import json
from django.core import serializers
import json

month = [
  'января',
  'февраля',
  'марта',
  'апреля',
  'мая',
  'июня',
  'июля',
  'августа',
  'сентября',
  'октября',
  'ноября',
  'декабря'
]


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def index(request):
    s = Article.objects.order_by('-pub_date')
    ln = len(s)
    addition = 2

    if is_ajax(request):
        print("AJAX")
        count = int(request.GET.get('count'))

        if count + addition >= ln:
            data = serializers.serialize('json', s[count:])
        else:
            data = serializers.serialize('json', s[count: count + addition])
        data = json.loads(data)
        for i in range(len(data)):
            tmp = data[i]['fields']['pub_date']
            tmp = tmp[tmp.rfind("-") + 1:] + " " + month[int(tmp[tmp.find("-") + 1:tmp.rfind("-")]) - 1] + " " + tmp[: tmp.find("-")] + " г."

            if tmp[0] == "0":
                tmp = tmp[1:]
            data[i]['fields']['pub_date'] = tmp

        return HttpResponse(json.dumps(data), content_type='application/json')
    # for i in s:
    #
    #     vk_likes.append(requests.get("https://api.vk.com/method/likes.getList?type=sitepage&owner_id=8192046&item_id=0&page_url=http://127.0.0.1:8000/article/" + str(i.id) +"/&filter=likes&access_token=vk1.a.5RsA-mkLp4fvjwSxikCVxVXrK8VSvDIBSI94B4pLLpaJVS7SGRzO1IG-Ufz_a8I99tx4es-qymwFLnqL89fLoynsNCRHCbkvUQiD47ntBVWIXu725Z167vxY2yK9jCb30OCEMPnUQq1LWYg91LuZs5l_d96WqfBRFsQmEjq5KyKl1vcV3cjTu5nz8NQuwkFF&v=5.131").text)
    #     vk_likes[-1] = json.loads(vk_likes[-1])["response"]["count"]
    # print(vk_likes)
    return render(request, "articles/index.html", {"articles": s[:4]})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# def one_article_old(request, id):
#     print(get_client_ip(request))
#     new = False
#     obj = Article.objects.filter(id=id)[0]
#     obj.views += 1
#     obj.save()
#
#     comments = obj.comments.filter(active=True)
#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#
#             if validate(new_comment.email) and len(comments.filter(email=new_comment.email, created__date=timezone.now().date())) < 5:
#                 new_comment.article = obj
#                 new_comment.save()
#                 new = True
#     else:
#         comment_form = CommentForm()
#
#     res = re.findall('(<[pq]>.*</[pq]>)|(<h2>.*</h2>)|(<img src=\"http.*\" alt=\".*\">)', obj.text)
#     tags = []
#     for i in res:
#         for ans in i:
#             if ans != "":
#                 if ans[1] == "p":
#                     tags.append({"type": "p", "text": ans[3:-4]})
#                 elif ans[1] == "h":
#                     tags.append({"type": "h2", "text": ans[4:-5]})
#                 elif ans[1] == "i":
#                     tags.append({"type": "img", "src": ans[ans.find("http"): ans.find('" alt')], "alt": ans[ans.find('alt="') + 5:-2]})
#                 elif ans[1] == "q":
#                     tags.append({"type": "q", "text": ans[3:-4]})
#
#     return render(request, "articles/one_index.html", {"tags": tags,
#                                                        "article": obj,
#                                                        'comments': comments,
#                                                        'comment_form': comment_form,
#                                                        'new': new})


def one_article(request, id):

    if is_ajax(request):
        data = request.POST.dict()
        obj = Article.objects.filter(id=id)[0]

        if obj.secret_key == data['secret_key']:
            if data['type'] == 'like':
                if int(data['value']) == 1:
                    obj.like_count += 1
                else:
                    obj.like_count -= 1
            else:
                if int(data['value']) == 1:
                    obj.comment_count += 1
                else:
                    obj.comment_count -= 1

            # obj.secret_key = Article.new_key()
            obj.save()
            return HttpResponse(status=200, content=200)
        return HttpResponse(status=500, content=500)


    print(get_client_ip(request))
    obj = Article.objects.filter(id=id)[0]
    obj.views += 1
    obj.secret_key = Article.new_key()
    obj.save()

    res = re.findall('(<[pq]>.*</[pq]>)|(<h2>.*</h2>)|(<img src=\"http.*\" alt=\".*\">)', obj.text)
    tags = []
    for i in res:
        for ans in i:
            if ans != "":
                if ans[1] == "p":
                    tags.append({"type": "p", "text": ans[3:-4]})
                elif ans[1] == "h":
                    tags.append({"type": "h2", "text": ans[4:-5]})
                elif ans[1] == "i":
                    tags.append({"type": "img", "src": ans[ans.find("http"): ans.find('" alt')], "alt": ans[ans.find('alt="') + 5:-2]})
                elif ans[1] == "q":
                    tags.append({"type": "q", "text": ans[3:-4]})

    return render(request, "articles/one_index.html", {"tags": tags,
                                                       "article": obj})


def theme_articles(request, theme):
    s = []
    for i in Article.objects.all():
        tmp = json.loads(i.themes)
        if theme in tmp:
            s.append(i)
    return render(request, "articles/index.html", {"articles": s})


def theme_view(request):
    themes = set()
    for obj in Article.objects.all():
        tmp = json.loads(obj.themes)
        for i in tmp:
            themes.add(i)
    print(themes)
    return render(request, "articles/themes_index.html", {"themes": themes})


def like_register(request, id, key, value):
    obj = Article.objects.filter(id=id)[0]

    print(obj.secret_key == key)
    if obj.secret_key == key:
        if value == 1:
            obj.like_count += 1
        else:
            obj.like_count -= 1
    obj.secret_key = Article.new_key()
    obj.save()

    return redirect("articles:one_article", id=id)


def comment_register(request, id, key, value):
    obj = Article.objects.filter(id=id)[0]

    print(obj.secret_key == key)
    if obj.secret_key == key:
        if value == 1:
            obj.comment_count += 1
        else:
            obj.comment_count -= 1
    obj.secret_key = Article.new_key()
    obj.save()

    return redirect("articles:one_article", id=id)

