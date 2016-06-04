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
from dzien_wydzialu.home.forms import VisitorGroupForm, AssignGroupForm

from weasyprint import HTML, CSS


def index(request):
    return render(request, "home/index.html", {})


def program(request):
    groups = Group.objects.all()
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
