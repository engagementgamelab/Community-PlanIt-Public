from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from admin.forms import AnswerForm
from admin.views import verify
from player_activities.models import PlayerActivity
from answers.models import Answer
from comments.forms import CommentForm


@login_required
def manage(request, activity_id, template="admin/manage_answers.html"):
    ok = verify(request)
    if ok != None:
        return ok

    try:
        activity = PlayerActivity.objects.untranslated().get(pk=int(activity_id))
    except PlayerActivity.DoesNotExist:
        raise Http404 ("PlayerActivity with id %s does not exist" % activity_id)

    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin:manage-answers", args=[activity_id]))

    data = {}
    for answer in Answer.objects.filter(activity=activity):
        for lang_code, _lang_name in settings.LANGUAGES:
            data[answer] = {'%s_comments' % lang_code: answer.comments.language(lang_code),}
        # 'en-us' variable does not work in html template because of '-'
        data[answer] = {'en_comments' : answer.comments.language('en-us'),}   
        
    comment_form = CommentForm(data=request.POST or None)      
    

    context = {
        'data' : data,        
        'activity': activity,
        'comment_form': comment_form
    }
    return render_to_response(template, RequestContext(request, context))


@login_required
def answer(request, activity_id, answer_id=None, template="admin/trans_answer_edit.html"):   
    is_new = False
    ok = verify(request)
    if ok != None:
        return ok

    try:
        activity = PlayerActivity.objects.untranslated().get(pk=int(activity_id))
    except PlayerActivity.DoesNotExist:
        raise Http404 ("PlayerActivity with id %s does not exist" % activity_id)

    if (request.POST.has_key("submit_btn") and request.POST["submit_btn"] == "Cancel"):
        return HttpResponseRedirect(reverse("admin:manage-answers", args=[activity_id]))

    if answer_id is not None and answer_id != 'None':
        answer = get_object_or_404(Answer, pk=int(answer_id))        
    else:
        answer = Answer(activity=activity)
        is_new = True

    errors = {}
    form = AnswerForm(instance=answer, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            try:               
                answer = form.save(commit=False)
                answer.activity = activity
                answer.save()
                return HttpResponseRedirect(reverse("admin:manage-answers", args=[activity_id]))
            except Exception, err:
                #transaction.rollback()
                print "error while saving answer: %s" % str(err)
                log.error("error while saving answer: %s" % str(err))
                errors.update({"Updating mission": "Server error took place. Please contact the admin."})
        else:
            if form.errors:
                errors.update(form.errors)
    context = {
            'activity': activity,            
            'answer_form': form,
            'answer': answer,
            'new': is_new,
            'errors': errors,
    }

    return render_to_response(template, RequestContext(request, context))
