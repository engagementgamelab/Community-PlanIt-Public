import re

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template import RequestContext, loader

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

import Image

from web.attachments.models import Attachment
from web.comments.forms import CommentForm
from web.comments.models import Comment
from web.games.models import Game, PlayerGame
from web.games.thinkfast.models import ThinkFast
from web.missions.models import Mission
from web.processors import instance_processor as ip
from web.reports.actions import PointsAssigner, ActivityLogger
from web.responses.choices.forms import ChoicesResponseForm
from web.responses.choices.models import *
from settings import MEDIA_ROOT

@login_required
def index(request, mission_slug, id):
    instance = request.user.get_profile().instance
    mission = Mission.objects.get(slug=mission_slug)
    game = get_object_or_404(Game, id=id)
    thinkfast = game.thinkfast

    if instance.is_expired() or mission.is_expired():
        return HttpResponseRedirect(reverse('games_thinkfast_overview', args=[mission_slug, id]))

    # Code to check for games not yet played
    unplayed = []
    _played = []

    player_game = None
    try:
        player_game = PlayerGame.objects.get(user=request.user, game=game)
        choices_form.fields['choices'].initial = player_game.response.choicesresponse.choices.all()[0].id
    except:
        choices_form = ChoicesResponseForm(instance=thinkfast.response)

    if request.method == 'POST':
        choices_form = ChoicesResponseForm(request.POST, instance=thinkfast.response)

        if choices_form.is_valid():
            try:
                player_game = PlayerGame.objects.get(user=request.user, game=game)
                player_game.delete()

                response = ChoicesResponse(answer=True)
                response.save()

                response.choices.add(choices_form.cleaned_data['choices'])
                response.save()

                player_game = PlayerGame(visible=True, completed=True, response=response, game=thinkfast, user=request.user)
                response = player_game.response.choicesresponse
                player_game.save()

                log_url = reverse('games_thinkfast_overview', args=[mission_slug, id])
                ActivityLogger.log(request.user, request, 'a ThinkFast! activity', 'updated', log_url, 'thinkfast')
            except:
                response = ChoicesResponse(answer=True)
                response.save()
                response.choices.add(choices_form.cleaned_data['choices'])
                response.save()
                player_game = PlayerGame(visible=True, completed=True, response=response, game=thinkfast, user=request.user)
                player_game.save()

                log_url = reverse('games_thinkfast_overview', args=[mission_slug, id])
                ActivityLogger.log(request.user, request, 'a ThinkFast! game', 'completed', log_url, 'thinkfast')
                PointsAssigner.assign(request.user, 'thinkfast_completed')

                request.session['justplayed'] = True

            games = mission.games.all()
            pg = PlayerGame.objects.filter(user=request.user, completed=True)
            for p in pg:
                _played.append(p.game)
            for g in games:
                if not g in _played and not g == game:
                    unplayed.append(g)

            return HttpResponseRedirect(reverse('games_thinkfast_overview', args=[mission_slug, id]))

    other_responses = PlayerGame.objects.all().filter(game=thinkfast, completed=True)
    
    fileList = []
    for x in thinkfast.prompt.attachments.all():
        fileName = "%s%s" % (settings.MEDIA_ROOT, x.file)
        #Manipulate this to get the image down to a 2:3aspect ratio so
        #200:300
        img = Image.open(fileName)
        x1 = img.size[0]
        y1 = img.size[1]
        fileList.append((x.file, x1, y1))
        
    
    tmpl = loader.get_template('games/thinkfast/index.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'unplayed': unplayed,
        'other_responses': other_responses[:5],
        'mission': mission,
        'game': game,
        'thinkfast': thinkfast,
        'choices_form': choices_form,
        'player_game': player_game,
        'fileList': fileList,
    }, [ip])))

@login_required
def overview(request, mission_slug, id):
    mission = Mission.objects.get(slug=mission_slug)
    game = Game.objects.get(id=id)
    thinkfast = game.thinkfast
    first_time = request.session.has_key('justplayed') and request.session['justplayed'] or False
    request.session['justplayed'] = False

    if not thinkfast.playergame_set.filter(user=request.user).count():
        messages.success(request, "You'll have to complete this activity to join its discussion.", extra_tags='sticky')
        return HttpResponseRedirect(reverse('games_thinkfast_index', args=[mission_slug, id]))

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = thinkfast.comments.create(
                message=comment_form.cleaned_data['message'], 
                user=request.user,
                instance=request.user.get_profile().instance,
            )

            if request.POST.has_key('yt-url'):
                url = request.POST.get('yt-url')
                if url:
                    comment.attachment.create(
                        file=None,
                        url=url,
                        type='video',
                        user=request.user,
                        instance=request.user.get_profile().instance,
                    )

            if request.FILES.has_key('picture'):
                comment.attachment.create(
                    file=request.FILES.get('picture'),
                    user=request.user,
                    instance=request.user.get_profile().instance,
                )

            PointsAssigner.assign(request.user, 'comment_created')
            log_url = reverse('games_thinkfast_overview', args=[mission_slug, id]) + '#comment-' + str(comment.pk)
            ActivityLogger.log(request.user, request, 'to ThinkFast! response', 'added comment', log_url, 'thinkfast')

            return HttpResponseRedirect(reverse('games_thinkfast_overview', args=[mission_slug, id]))
    else:
        comment_form = CommentForm()

    other_responses = PlayerGame.objects.all().filter(game=thinkfast, completed=True)

    responses_wrapper = []
    total_responses = 0

    choices = {}
    for pg in other_responses:
        player = pg.user
        label = pg.response.choicesresponse.choices.all()[0].text
        total_responses += 1
        if choices.has_key(label):
            choices[label].append(player)
        else:
            choices[label] = [player]

    for choice, players in choices.items():
        # +0.0 coerces to a float for percentages
        responses_wrapper.append({ 'choice': choice, 'players': len(players), 
                                  'percent': 0 if total_responses == 0 else ((len(players)+0.0)/total_responses)*100 })
    
    unplayed = []
    _played = []
    games = mission.games.all()
    pg = PlayerGame.objects.filter(user=request.user, completed=True)
    for p in pg:
        _played.append(p.game)
    for g in games:
        if not g in _played and not g == game:
            unplayed.append(g)
    
    if len(unplayed):
        unplayed = unplayed[0]
    
    fileList = []
    for x in thinkfast.prompt.attachments.all():
        fileName = "%s%s" % (MEDIA_ROOT, x.file)
        #Manipulate this to get the image down to a 2:3aspect ratio so
        #200:300
        img = Image.open(fileName)
        x1 = img.size[0]
        y1 = img.size[1]
        fileList.append((x.file, x1, y1))
    
    tmpl = loader.get_template('games/thinkfast/overview.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'other_responses': other_responses[:5],
        'response': thinkfast.response.choicesresponse,
        'responses_wrapper': responses_wrapper,
        'choices': choices,
        'mission': mission,
        'game': game,
        'thinkfast': thinkfast,
        'unplayed': unplayed,
        'first_time': first_time,
        'total_responses' : total_responses,
        'fileList': fileList,
    }, [ip])))

@login_required
def response(request, mission_slug, id, user_id):
    mission = Mission.objects.get(slug=mission_slug)
    game = Game.objects.get(id=id)
    thinkfast = game.thinkfast
    user = User.objects.get(id=user_id)

    player_game = PlayerGame.objects.get(user=user, game=game)

    other_responses = PlayerGame.objects.all().filter(game=thinkfast, completed=True)

    tmpl = loader.get_template('games/thinkfast/response.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'other_responses': other_responses[:5],
        'mission': mission,
        'game': game,
        'thinkfast': thinkfast,
        'user': user,
        'player_game': player_game,
        'comments': player_game,
        'response': player_game.response.choicesresponse.choices.all()[0].text,
        'comment_form': CommentForm(),
    }, [ip])))

