import web, re
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from web.missions.models import Mission
from web.games.models import Game, PlayerGame
from web.games.thinkfast.models import ThinkFast
from web.responses.choices.models import *
from web.responses.choices.forms import ChoicesResponseForm
from web.attachments.models import Attachment
from web.comments.models import Comment
from web.comments.forms import CommentForm
from web.reports.actions import PointsAssigner, ActivityLogger
from web.processors import instance_processor as ip

@login_required
def index(request, mission_slug, id):
    instance = request.user.get_profile().instance
    mission = Mission.objects.get(slug=mission_slug)
    game = get_object_or_404(Game, id=id)
    thinkfast = game.thinkfast

    if instance.is_expired() or mission.is_expired():
        return HttpResponseRedirect('/mission/'+ mission_slug +'/game/thinkfast/'+ id +'/overview/')

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

                ActivityLogger.log(request.user, request, 'a ThinkFast! activity', 'updated', '/mission/'+ mission_slug +'/game/thinkfast/'+ id +'/'+str(request.user.id), 'thinkfast')
            except:
                response = ChoicesResponse(answer=True)
                response.save()
                response.choices.add(choices_form.cleaned_data['choices'])
                response.save()
                player_game = PlayerGame(visible=True, completed=True, response=response, game=thinkfast, user=request.user)
                player_game.save()
                ActivityLogger.log(request.user, request, 'a ThinkFast! activity', 'completed', '/mission/'+ mission_slug +'/game/thinkfast/'+ id +'/'+str(request.user.id), 'thinkfast')
                PointsAssigner.assign(request.user, 'thinkfast_completed')

                request.session['justplayed'] = True

            games = mission.games.all()
            pg = PlayerGame.objects.filter(user=request.user, completed=True)
            for p in pg:
                _played.append(p.game)
            for g in games:
                if not g in _played and not g == game:
                    unplayed.append(g)

            return HttpResponseRedirect(request.path +'overview')

    other_responses = PlayerGame.objects.all().filter(game=thinkfast, completed=True)

    tmpl = loader.get_template('games/thinkfast/index.html')
    return HttpResponse(tmpl.render(RequestContext(request, {
        'unplayed': unplayed,
        'other_responses': other_responses[:5],
        'mission': mission,
        'game': game,
        'thinkfast': thinkfast,
        'choices_form': choices_form,
        'player_game': player_game,
    }, [ip])))

@login_required
def comment(request, mission_slug, id, user_id):
    a = None
    b = None

    mission = Mission.objects.get(slug=mission_slug)
    game = Game.objects.get(id=id)
    thinkfast = game.thinkfast
    user = User.objects.get(id=user_id)

    player_game = PlayerGame.objects.filter(user=user, game=game)
    if len(player_game) > 1:
        for pg in player_game[0:len(player_game)-1]:
            pg.delete()

    player_game = player_game[0]
    instance = request.user.get_profile().instance

    if request.method == 'POST':
        if request.POST.has_key('yt-url'):
            if request.POST.get('yt-url'):
                url = re.search(r"(?<=v=)[a-zA-Z0-9-]+(?=&)|(?<=[0-9]/)[^&\n]+|(?<=v=)[^&\n]+", request.POST.get('yt-url')).group()

                if len(url) > 1:
                    a = Attachment(
                        file=None,
                        url=url,
                        type='video',
                        user=request.user,
                        instance=request.user.get_profile().instance,
                    )
                    a.save()
        
        if request.FILES.has_key('picture'):
            b = Attachment(
                file=request.FILES.get('picture'),
                user=request.user,
                instance=request.user.get_profile().instance,
            )

            b.save()

        form = CommentForm(request.POST)
        if form.is_valid():
            c = Comment(
                message=form.cleaned_data['message'], 
                user=request.user,
                instance=instance,
            )
            c.save()

            if a:
                c.attachment.add(a)
                c.save()

            if b:
                c.attachment.add(b)
                c.save()

            player_game.comments.add(c)
            player_game.save()

            PointsAssigner.assign(request.user, 'comment_created')
            ActivityLogger.log(request.user, request, 'to ThinkFast! response', 'added comment', '/mission/'+ mission_slug +'/game/thinkfast/'+ id +'/'+ user_id, 'thinkfast')

    return HttpResponseRedirect('/mission/'+ mission_slug +'/game/thinkfast/'+ id +'/'+ user_id)

@login_required
def overview(request, mission_slug, id):
    mission = Mission.objects.get(slug=mission_slug)
    game = Game.objects.get(id=id)
    thinkfast = game.thinkfast
    first_time = request.session.has_key('justplayed') and request.session['justplayed'] or False
    request.session['justplayed'] = False

    other_responses = PlayerGame.objects.all().filter(game=thinkfast, completed=True)

    responses_wrapper = []
    total_responses = 0

    # Calculate total coins for next iteration to generate percentages
    #for issue in issues:
    #    player_issue = playerissues.filter(issue=issue)
    #    if len(player_issue) > 0:
    #        total_coins += player_issue[0].coins

    #for issue in issues:
    #    player_issue = playerissues.filter(issue=issue)
    #    if len(player_issue) > 0:
    #        coins = player_issue[0].coins

    #        # +0.0 coerces to a float for percentages
    #        issue_wrapper.append({ 'issue': issue, 'player_coins': coins, 'percent': ((coins+0.0)/total_coins)*100 })
    #    else:
    #        issue_wrapper.append({ 'issue': issue, 'player_coins': 0, 'percent': 0 })

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
        responses_wrapper.append({ 'choice': choice, 'players': len(players), 'percent': ((len(players)+0.0)/total_responses)*100 })
    
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
