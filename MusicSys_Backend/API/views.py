import datetime
import time
from io import BufferedReader
import jwt
import requests
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import F
from django.http import JsonResponse, QueryDict
from django.views import View
from API.models import MusicModel, CollectModel, CommentModel, UserModel, AdminModel


# Create your views here.
class UserView(View):
    def get(self, request):
        username = request.GET.get('username') if request.GET.get('username') else ''
        nickname = request.GET.get('nickname') if request.GET.get('nickname') else ''
        pageNum = request.GET.get('pageNum') if request.GET.get('pageNum') else 1
        pageSize = request.GET.get('pageSize') if request.GET.get('pageSize') else 20

        userModel = UserModel.objects.filter(username__icontains=username, nickname__icontains=nickname).order_by('id')
        total = userModel.count()

        paginator = Paginator(userModel, pageSize)
        page_obj = paginator.get_page(pageNum)
        userList = list(page_obj.object_list.values())

        rdd = {'data': {'user': userList, 'total': total}}

        return JsonResponse(rdd, content_type='application/json')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')
        iconUrl = settings.UPLOAD_ROOT + 'iconUrl/default_avatar.jpg'

        userModel = UserModel.objects.all()

        if username and password and nickname and email and iconUrl:
            if userModel.filter(username=username).exists():
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '用户已存在'}}
            else:
                addTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                user = UserModel()
                user.username = username
                user.password = password
                user.nickname = nickname
                user.email = email
                user.iconUrl = iconUrl
                user.addTime = addTime
                user.save()

                dd = {'id': user.id, 'username': username, 'nickname': nickname, 'email': email, 'iconUrl': iconUrl,
                      'addTime': addTime}
                rdd = {'data': dd, 'meta': {'status': 201, 'msg': '注册成功'}}

        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')

    def put(self, request):
        id = QueryDict(request.body).get('id')
        nickname = QueryDict(request.body).get('nickname')
        email = QueryDict(request.body).get('email')
        iconUrl = QueryDict(request.body).get('iconUrl')

        userModel = UserModel.objects.all()

        if id:
            user = userModel.get(id=id)
            user.nickname = nickname
            user.email = email
            user.iconUrl = iconUrl
            user.save()

            dd = {'id': id, 'username': user.username, 'nickname': nickname, 'email': email, 'iconUrl': iconUrl}
            rdd = {'data': dd, 'meta': {'status': 201, 'msg': '修改用户信息成功'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')

    def delete(self, request):
        id = QueryDict(request.body).get('id')

        userModel = UserModel.objects.all()

        if id:
            userModel.get(id=id).delete()
            rdd = {'data': None, 'meta': {'status': 204, 'msg': '删除用户成功'}}
        else:
            ids = QueryDict(request.body).getlist('id[]')
            if ids:
                userModel.filter(pk__in=ids).delete()
                rdd = {'data': None, 'meta': {'status': 204, 'msg': '删除用户成功'}}
            else:
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')


class UserLoginView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = UserModel.objects.filter(username=username)
            if user.exists():
                if user.values()[0]['password'] == password:
                    user.update(loginTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    user = user.values()[0]
                    headers = {
                        'typ': 'jwt',
                        'alg': 'HS256'
                    }
                    payload = {
                        'id': user['id'],
                    }
                    token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256', headers=headers)
                    rdd = {'data': {'token': token}, 'meta': {'status': 201, 'msg': '操作成功'}}
                else:
                    rdd = {'data': None, 'meta': {'status': 400, 'msg': '密码错误'}}
            else:
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '用户不存在'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')


class UserInfoView(View):
    def get(self, request):
        token = request.GET.get('token')

        if token:
            id = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms='HS256')['id']
            userInfo = UserModel.objects.get(id=id).__str__()
            rdd = {'data': userInfo, 'meta': {'status': 200, 'msg': '操作成功'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')


class UserPwdView(View):
    def get(self, request):
        id = request.GET.get('id')
        oldPassword = request.GET.get('oldPassword')

        userModel = UserModel.objects.get(id=id)

        if id:
            if userModel.password == oldPassword:
                rdd = {'data': None, 'meta': {'status': 200, 'msg': '密码正确'}}
            else:
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '密码错误'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')

    def post(self, request):
        id = request.POST.get('id')
        checkPassword = request.POST.get('checkPassword')

        if id:
            UserModel.objects.filter(id=id).update(password=checkPassword)
            rdd = {'data': None, 'meta': {'status': 201, 'msg': '修改成功'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')

    def put(self, request):
        id = QueryDict(request.body).get('id')

        userModel = UserModel.objects.all()

        if id:
            userModel.filter(id=id).update(password=123456)
            rdd = {'data': None, 'meta': {'status': 201, 'msg': '修改成功'}}
        else:
            ids = QueryDict(request.body).get('id[]')
            if ids:
                userModel.filter(pk__in=ids).update(password=123456)
                rdd = {'data': None, 'meta': {'status': 201, 'msg': '修改成功'}}
            else:
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')


class AdminLoginView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            admin = AdminModel.objects.filter(username=username)
            if admin.exists():
                if admin.values()[0]['password'] == password:
                    admin.update(loginTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    user = admin.values()[0]
                    headers = {
                        'typ': 'jwt',
                        'alg': 'HS256'
                    }
                    payload = {
                        'id': user['id'],
                    }
                    token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256', headers=headers)
                    rdd = {'data': {'token': token}, 'meta': {'status': 201, 'msg': '操作成功'}}
                else:
                    rdd = {'data': None, 'meta': {'status': 400, 'msg': '密码错误'}}
            else:
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '用户不存在'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')


class AdminPwdView(View):
    def get(self, request):
        id = request.GET.get('id')
        oldPassword = request.GET.get('oldPassword')

        adminModel = AdminModel.objects.get(id=id)

        if id:
            if adminModel.password == oldPassword:
                rdd = {'data': None, 'meta': {'status': 200, 'msg': '密码正确'}}
            else:
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '密码错误'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')

    def post(self, request):
        id = request.POST.get('id')
        checkPassword = request.POST.get('checkPassword')

        if id:
            AdminModel.objects.filter(id=id).update(password=checkPassword)
            rdd = {'data': None, 'meta': {'status': 200, 'msg': '修改成功'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')


class MusicView(View):
    def get(self, request):
        songName = request.GET.get('songName') if request.GET.get('songName') else ''
        singer = request.GET.get('singer') if request.GET.get('singer') else ''
        album = request.GET.get('album') if request.GET.get('album') else ''
        pageNum = request.GET.get('pageNum') if request.GET.get('pageNum') else 1
        pageSize = request.GET.get('pageSize') if request.GET.get('pageSize') else 20

        music = MusicModel.objects.filter(songName__icontains=songName, singer__icontains=singer,
                                          album__icontains=album).order_by('id')
        total = music.count()

        paginator = Paginator(music, pageSize)
        page_obj = paginator.get_page(pageNum)
        songList = list(page_obj.object_list.values())

        rdd = {'data': {'songs': songList, 'total': total}, 'meta': {'status': 200, 'msg': '操作成功'}}

        return JsonResponse(rdd, content_type='application/json')

    def post(self, request):
        songName = request.POST.get('songName')
        singer = request.POST.get('singer')
        album = request.POST.get('album')
        songTime = request.POST.get('songTime')
        lyric = request.POST.get('lyric')
        lyricist = request.POST.get('lyricist')
        picUrl = request.POST.get('picUrl')
        songUrl = request.POST.get('songUrl')

        music = MusicModel.objects.all()

        if songName and singer and album and songTime and picUrl and songUrl:
            if music.filter(songName=songName, singer=singer).exists():
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '歌曲已存在'}}
            else:
                addTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                song = MusicModel()
                song.songName = songName
                song.singer = singer
                song.album = album
                song.songTime = songTime
                song.lyric = lyric
                song.lyricist = lyricist
                song.picUrl = picUrl
                song.songUrl = songUrl
                song.addTime = addTime
                song.save()

                dd = {'id': song.id, 'songName': songName, 'singer': singer, 'album': album, 'songTime': songTime,
                      'lyric': lyric, 'lyricist': lyricist, 'picUrl': picUrl, 'songUrl': songUrl, 'addTime': addTime}
                rdd = {'data': dd, 'meta': {'status': 201, 'msg': '添加歌曲成功'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')

    def put(self, request):
        id = QueryDict(request.body).get('id')
        songName = QueryDict(request.body).get('songName')
        singer = QueryDict(request.body).get('singer')
        album = QueryDict(request.body).get('album')
        songTime = QueryDict(request.body).get('songTime')
        lyric = QueryDict(request.body).get('lyric')
        lyricist = QueryDict(request.body).get('lyricist')
        picUrl = QueryDict(request.body).get('picUrl')
        songUrl = QueryDict(request.body).get('songUrl')

        music = MusicModel.objects.all()

        if id:
            if music.filter(songName=songName, singer=singer).exists():
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '歌曲已存在'}}
            else:
                song = music.get(id=id)
                song.songName = songName
                song.singer = singer
                song.album = album
                song.songTime = songTime
                song.lyric = lyric
                song.lyricist = lyricist
                song.picUrl = picUrl
                song.songUrl = songUrl
                song.save()

                dd = {'id': song.id, 'songName': songName, 'singer': singer, 'album': album, 'songTime': songTime,
                      'lyric': lyric, 'lyricist': lyricist, 'picUrl': picUrl, 'songUrl': songUrl}
                rdd = {'data': dd, 'meta': {'status': 201, 'msg': '修改歌曲成功'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')

    def delete(self, request):
        id = QueryDict(request.body).get('id')

        musicModel = MusicModel.objects.all()

        if id:
            musicModel.get(id=id).delete()
            rdd = {'data': None, 'meta': {'status': 204, 'msg': '删除歌曲成功'}}
        else:
            ids = QueryDict(request.body).getlist('id[]')
            if ids:
                musicModel.filter(pk__in=ids).delete()
                rdd = {'data': None, 'meta': {'status': 204, 'msg': '删除歌曲成功'}}
            else:
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')


class MusicById(View):
    def get(self, request):
        id = request.GET.get('id')

        if id:
            song = MusicModel.objects.filter(id=id)
            if song.exists():
                song = song.values()[0]
                rdd = {'data': song, 'meta': {'status': 200, 'msg': '操作成功'}}
            else:
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '歌曲不存在'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')


class CollectView(View):
    def get(self, request):
        username = request.GET.get('username') if request.GET.get('username') else ''
        songName = request.GET.get('songName') if request.GET.get('songName') else ''
        singer = request.GET.get('singer') if request.GET.get('singer') else ''
        album = request.GET.get('album') if request.GET.get('album') else ''
        pageNum = request.GET.get('pageNum') if request.GET.get('pageNum') else 1
        pageSize = request.GET.get('pageSize') if request.GET.get('pageSize') else 20

        collectModel = CollectModel.objects.filter(
            user__username__icontains=username, music__songName__icontains=songName, music__singer__icontains=singer,
            music__album__icontains=album).values(
            'id', 'addTime', username=F('user__username'), songName=F('music__songName'), singer=F('music__singer'),
            album=F('music__album'), songTime=F('music__songTime'), lyric=F('music__lyric'), picUrl=F('music__picUrl'),
            songUrl=F('music__songUrl')).order_by('id')
        total = collectModel.count()

        paginator = Paginator(collectModel, pageSize)
        page_obj = paginator.get_page(pageNum)
        collectList = list(page_obj.object_list)

        rdd = {'data': {'collect': collectList, 'total': total}}

        return JsonResponse(rdd, content_type='application/json')

    def post(self, request):
        user_id = request.POST.get('user_id')
        music_id = request.POST.get('user_id')

        collectModel = CollectModel.objects.all()

        if user_id and music_id:
            if collectModel.filter(user_id=user_id, music_id=music_id).exists():
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '该歌曲已收藏'}}
            else:
                addTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                col = CollectModel()
                col.user_id = user_id
                col.music_id = music_id
                col.addTime = addTime
                col.save()

                dd = {'id': col.id, 'user_id': user_id, 'music_id': music_id, 'addTime': addTime}
                rdd = {'data': dd, 'meta': {'status': 201, 'msg': '收藏成功'}}

        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')

    def delete(self, request):
        id = QueryDict(request.body).get('id')

        collectModel = CollectModel.objects.all()

        if id:
            collectModel.get(id=id).delete()
            rdd = {'data': None, 'meta': {'status': 204, 'msg': '取消收藏成功'}}
        else:
            ids = QueryDict(request.body).getlist('id[]')
            if ids:
                collectModel.filter(pk__in=ids).delete()
                rdd = {'data': None, 'meta': {'status': 204, 'msg': '取消收藏成功'}}
            else:
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')


class CommentView(View):
    def get(self, request):
        username = request.GET.get('username') if request.GET.get('username') else ''
        songName = request.GET.get('songName') if request.GET.get('songName') else ''
        pageNum = request.GET.get('pageNum') if request.GET.get('pageNum') else 1
        pageSize = request.GET.get('pageSize') if request.GET.get('pageSize') else 20

        commentModel = CommentModel.objects.filter(
            user__username__icontains=username, music__songName__icontains=songName).values(
            'id', 'comment', 'addTime', username=F('user__username'), iconUrl=F('user__iconUrl'),
            songName=F('music__songName')).order_by('id')
        total = commentModel.count()

        paginator = Paginator(commentModel, pageSize)
        page_obj = paginator.get_page(pageNum)
        collectList = list(page_obj.object_list)

        rdd = {'data': {'comment': collectList, 'total': total}, 'meta': {'status': 200, 'msg': '操作成功'}}

        return JsonResponse(rdd, content_type='application/json')

    def post(self, request):
        user_id = request.POST.get('user_id')
        music_id = request.POST.get('user_id')
        comment = request.POST.get('comment')

        if user_id and music_id:
            addTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            col = CommentModel()
            col.user_id = user_id
            col.music_id = music_id
            col.comment = comment
            col.addTime = addTime
            col.save()

            dd = {'id': col.id, 'user_id': user_id, 'music_id': music_id, 'comment': comment, 'addTime': addTime}
            rdd = {'data': dd, 'meta': {'status': 201, 'msg': '评论成功'}}

        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')

    def put(self, request):
        id = QueryDict(request.body).get('id')
        comment = QueryDict(request.body).get('comment')

        commentModel = CommentModel.objects.all()

        if id:
            com = commentModel.get(id=id)
            com.comment = comment
            com.save()

            dd = {'id': id, 'user_id': com.user_id, 'music_id': com.music_id, 'comment': comment}
            rdd = {'data': dd, 'meta': {'status': 201, 'msg': '修改评论成功'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')

    def delete(self, request):
        id = QueryDict(request.body).get('id')

        commentModel = CommentModel.objects.all()

        if id:
            commentModel.get(id=id).delete()
            rdd = {'data': None, 'meta': {'status': 204, 'msg': '删除评论成功'}}
        else:
            ids = QueryDict(request.body).getlist('id[]')
            if ids:
                commentModel.filter(pk__in=ids).delete()
                rdd = {'data': None, 'meta': {'status': 204, 'msg': '删除评论成功'}}
            else:
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')


class CommentByMusicId(View):
    def get(self, request):
        music_id = request.GET.get('music_id')
        pageNum = request.GET.get('pageNum') if request.GET.get('pageNum') else 1
        pageSize = request.GET.get('pageSize') if request.GET.get('pageSize') else 20

        if music_id:
            commentModel = CommentModel.objects.filter(music_id=music_id).values(
                'id', 'comment', 'addTime', username=F('user__username'), iconUrl=F('user__iconUrl'),
                songName=F('music__songName')).order_by('id')
            total = commentModel.count()

            paginator = Paginator(commentModel, pageSize)
            page_obj = paginator.get_page(pageNum)
            collectList = list(page_obj.object_list)

            rdd = {'data': {'comment': collectList, 'total': total}, 'meta': {'status': 200, 'msg': '操作成功'}}
        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')


class CarouselView(View):
    def get(self, request):
        ids = [181, 182, 183, 184]
        carouselList = list(MusicModel.objects.filter(id__in=ids).values())

        rdd = {'data': carouselList, 'meta': {'status': 200, 'msg': '操作成功'}}

        return JsonResponse(rdd, content_type='application/json')


class NewSongsView(View):
    def get(self, request):
        newSongsList = list(MusicModel.objects.all()[:20].values())

        rdd = {'data': newSongsList, 'meta': {'status': 200, 'msg': '操作成功'}}

        return JsonResponse(rdd, content_type='application/json')


class TopSongsView(View):
    def get(self, request):
        ids = [1, 2, 9, 11, 6, 3, 16, 7, 5, 8]
        topSongsList = list(MusicModel.objects.filter(id__in=ids).values())

        rdd = {'data': topSongsList, 'meta': {'status': 200, 'msg': '操作成功'}}

        return JsonResponse(rdd, content_type='application/json')


class UploadView(View):
    def post(self, request):
        file = request.FILES
        filename = str(round(time.time() * 1000))
        if file:
            if 'picFile' in file.keys():
                content = BufferedReader(file.get('picFile'))
                suffix = '.' + content.name.split('.')[-1]
                url = settings.UPLOAD_ROOT + 'picUrl/' + filename + suffix
                response = requests.put(url, data=content)
                if response.status_code == 201:
                    rdd = {'data': {'picUrl': url}, 'meta': {'status': 201, 'msg': '上传专辑封面成功'}}
                else:
                    rdd = {'data': None, 'meta': {'status': 400, 'msg': '上传专辑封面失败'}}

            elif 'audioFile' in file.keys():
                content = BufferedReader(file.get('audioFile'))
                suffix = '.' + content.name.split('.')[-1]
                url = settings.UPLOAD_ROOT + 'musicUrl/' + filename + suffix
                response = requests.put(url, data=content)
                if response.status_code == 201:
                    rdd = {'data': {'songUrl': url}, 'meta': {'status': 201, 'msg': '上传音频成功'}}
                else:
                    rdd = {'data': None, 'meta': {'status': 400, 'msg': '上传音频失败'}}

            elif 'iconUrl' in file.keys():
                content = BufferedReader(file.get('iconUrl'))
                suffix = '.' + content.name.split('.')[-1]
                url = settings.UPLOAD_ROOT + 'iconUrl/' + filename + suffix
                response = requests.put(url, data=content)
                if response.status_code == 201:
                    rdd = {'data': {'picUrl': url}, 'meta': {'status': 201, 'msg': '上传头像成功'}}
                else:
                    rdd = {'data': None, 'meta': {'status': 400, 'msg': '上传头像失败'}}

            else:
                rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        else:
            rdd = {'data': None, 'meta': {'status': 400, 'msg': '参数错误'}}

        return JsonResponse(rdd, content_type='application/json')
