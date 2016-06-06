from django.db.models import Q
from django.shortcuts import render
from dzien_wydzialu.home.models import Group, Image, VisitorGroup
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.decorators.http import require_POST
from django.forms.models import formset_factory
from dzien_wydzialu.home.forms import VisitorGroupForm, AssignGroupForm, SurveyAccessForm, SurveyAnswerForm, SurveyAnswerFormsetHelper
from dzien_wydzialu.home.models import SurveyCode, Activity, Lecturer
from functools import partial, wraps


from weasyprint import HTML, CSS


def index(request):
    return render(request, "home/index.html", {})


def program(request):
    groups = Group.objects.all()
    assignform = None
    if request.user.is_authenticated():
        group_caretaker = Q(caretaker=request.user)
        group_unassigned = Q(assigned_group=None)
        assignform = AssignGroupForm(
            queryset=VisitorGroup.objects.filter(group_caretaker &
                                                 group_unassigned))
    return render(request, "home/program.html", {
                  'groups': groups,
                  'assignform': assignform,
                  })


def gallery(request):
    images = Image.objects.all()
    return render(request, "home/gallery.html", {"images": images})


def get_group_pdf(request, group_id):
    html_template = get_template('home/group_details.html')
    group = Group.objects.get(pk=group_id)

    ctx = RequestContext(request, {'group': group})
    rendered_html = html_template.render(ctx).encode(encoding="UTF-8")

    stylesheet = CSS(settings.BASE_DIR + '/dzien_wydzialu/home' +
                     static('css/custom.css'))
    pdf_file = HTML(string=rendered_html).write_pdf(stylesheets=[stylesheet])

    http_response = HttpResponse(pdf_file, content_type='application/pdf')
    http_response['Content-Disposition'] = 'filename="report.pdf"'

    return http_response


@login_required
def visitorgroup_index(request):
    visitorgroups = request.user.visitorgroup_set.all().order_by('id')
    return render(request, "home/visitorgroup_index.html", {
                  'visitorgroups': visitorgroups,
                  })


@login_required
def visitorgroup_new(request):
    if request.method == 'POST':
        form = VisitorGroupForm(request.POST)
        if form.is_valid():
            visitorgroup = form.save(commit=False)
            visitorgroup.caretaker = request.user
            visitorgroup.save()
            return HttpResponseRedirect(reverse('visitorgroup_index'))
    else:
        form = VisitorGroupForm()
    return render(request, "home/visitorgroup_new.html", {
                  'form': form,
                  })


@require_POST
@login_required
def visitorgroup_assign(request):
    form = AssignGroupForm(request.POST,
                           queryset=VisitorGroup.objects.filter(caretaker=request.user))
    group = form.data['group']
    if form.is_valid():
        visitorgroup = form.cleaned_data['visitorgroup']
        group_to_assign = Group.objects.get(pk=group)
        visitorgroup.assigned_group = group_to_assign
        visitorgroup.save()
    return HttpResponseRedirect(reverse('visitorgroup_index'))


@login_required
def visitorgroup_delete(request, visitorgroup_id):
    visitorgroup = VisitorGroup.objects.get(pk=visitorgroup_id)
    visitorgroup.delete()
    return HttpResponseRedirect(reverse('visitorgroup_index'))


@login_required
def visitorgroup_edit(request, visitorgroup_id):
    visitorgroup = VisitorGroup.objects.get(pk=visitorgroup_id)
    if request.method == 'POST':
        form = VisitorGroupForm(request.POST, instance=visitorgroup)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('visitorgroup_index'))
    else:
        form = VisitorGroupForm(instance=visitorgroup)
    form.helper.form_action = reverse('visitorgroup_edit',
                                      args=[visitorgroup_id])
    return render(request, "home/visitorgroup_edit.html", {
                  'form': form,
                  })


@login_required
def visitorgroup_unassign(request, visitorgroup_id):
    visitorgroup = VisitorGroup.objects.get(pk=visitorgroup_id)
    visitorgroup.assigned_group = None
    visitorgroup.save()
    return HttpResponseRedirect(reverse('visitorgroup_index'))


def access_survey(request):
    if request.method == 'POST':
        form = SurveyAccessForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                survey_code = SurveyCode.objects.get(code=code)
                if survey_code.used:
                    raise "used"
                request.session['survey_code'] = survey_code.code
                return HttpResponseRedirect(reverse(
                    'survey', args=[survey_code.group.id]))
            except:
                form.add_error(None, "Kod jest nieprawidłowy lub został już wykorzystany.")
    else:
        form = SurveyAccessForm()
    return render(request, "home/access_survey.html", {
                  'form': form,
                  })


def survey(request, group_id):
    code = request.session.get('survey_code', None)
    valid = False
    if code:
        try:
            survey_code = SurveyCode.objects.get(code=code)
            valid = True
        except:
            pass
    if not valid:
        return HttpResponseRedirect(reverse('access_survey'))

    group = Group.objects.get(pk=group_id)
    SurveyFormset = formset_factory(SurveyAnswerForm, extra=0)
    if request.method == 'POST':
        formset = SurveyFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
            try:
                del request.session['survey_code']
            except KeyError:
                pass
            survey_code.used = True
            survey_code.save()
            return HttpResponseRedirect(reverse('survey_thankyou'))
    else:
        initial = []
        for event in group.event_set.all():
            initial.append({'group': group, 'activity': event.activity})
        formset = SurveyFormset(initial=initial)
        for form in formset:
            form.fields['answer'].label = form.initial['activity'].title
    formset_helper = SurveyAnswerFormsetHelper(group_id=group_id)
    return render(request, "home/survey.html", {
                  'formset': formset,
                  'formset_helper': formset_helper,
                  })


def survey_thankyou(request):
    return render(request, "home/survey_thankyou.html", {})


def activity_detail(request, activity_id):
    activity = Activity.objects.get(pk=activity_id)
    return render(request, "home/activity_detail.html", {
                  'activity': activity,
                  })


def lecturer_detail(request, lecturer_id):
    lecturer = Lecturer.objects.get(pk=lecturer_id)
    return render(request, "home/lecturer_detail.html", {
                  'lecturer': lecturer,
                  })
