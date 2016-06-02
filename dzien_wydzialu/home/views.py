from django.shortcuts import render
from dzien_wydzialu.home.models import Group, Image, VisitorGroup
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.templatetags.staticfiles import static
from dzien_wydzialu.home.forms import VisitorGroupForm, AssignGroupForm

from weasyprint import HTML, CSS


def index(request):
    return render(request, "home/index.html", {})


def program(request):
    groups = Group.objects.all()
    assignform = AssignGroupForm(queryset=VisitorGroup.objects.filter(caretaker=request.user))
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
    visitorgroups = request.user.visitorgroup_set.all()
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


@login_required
def visitorgroup_assign(request):
    pass
