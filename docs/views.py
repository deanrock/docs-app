import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_user
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from docs.models import Project, get_url, Page, Version
from externals.restdown import restdown_path


@login_required
def view(request, project_url, page_url):
    project = Project.objects.filter(url=project_url).first()
    page = Page.objects.filter(url=page_url, project=project).first()

    if not project or not page:
        return HttpResponseRedirect(reverse('home'))

    version = Version.objects.filter(page=page).order_by('-id').first()

    if not version:
        return HttpResponseRedirect(reverse('edit', kwargs={
            'project_url' :project.url,
            'page_url': page.url
        }))

    content = version.content

    content, json = restdown_path(content)

    return render(request, 'view.html', {
        "project": project,
        "page": page,
        "version": version,
        "content": content,
    })


@login_required
def edit(request, project_url, page_url):
    project = Project.objects.filter(url=project_url).first()
    page = Page.objects.filter(url=page_url, project=project).first()
    version = Version.objects.filter(page=page).order_by('-id').first()

    if not project or not page:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        content = request.POST.get('content')

        if content and len(content) >= 3:
            #try to render before saving
            #better to crash before save than when serving page!
            _, _ = restdown_path(content)

            version = Version()
            version.added_at = datetime.datetime.now()
            version.added_by = request.user
            version.page = page
            version.content = content
            version.save()

            return HttpResponseRedirect(reverse('view', kwargs={
            'project_url' :project.url,
            'page_url': page.url
        }))

    return render(request, 'edit.html', {
        "project": project,
        "page": page,
        "version": version,
    })

@login_required
def get_last_version(request, project_url, page_url):
    project = Project.objects.filter(url=project_url).first()
    page = Page.objects.filter(url=page_url, project=project).first()

    if not project or not page:
        return HttpResponse(status=400)

    version = Version.objects.filter(page=page).order_by('-id').first()

    return JsonResponse({'version_id': version.id})

@login_required
def preview(request):
    if request.method == 'POST' and 'content' in request.POST:
        content, _ = restdown_path(request.POST['content'])

        return JsonResponse({'content': content})
    else:
        return HttpResponse(status=400)


@login_required
def home(request):
    if request.method == 'POST':
        project_name = request.POST.get('name', None)

        if project_name and len(project_name) >= 3:
            projects = Project.objects.filter(name=project_name)

            if projects:
                return HttpResponseRedirect(reverse('home'))

            project = Project()
            project.name = project_name
            project.added_at = datetime.datetime.now()
            project.added_by = request.user
            project.url = get_url(Project, project.name)

            project.save()

            return HttpResponseRedirect(reverse('home'))

        page_name = request.POST.get('pagename', None)
        project_id = request.POST.get('project_id', None)

        if page_name and len(page_name) >= 3 and project_id \
                and len(project_id) > 0:
            projects = Project.objects.filter(id=project_id)

            if not projects:
                return HttpResponseRedirect(reverse('home'))

            page = Page.objects.filter(project=projects.first(),
                                       title=page_name).first()

            if page:
                return HttpResponseRedirect(reverse('home'))

            page = Page()
            page.title = page_name
            page.project = projects.first()
            page.added_at = datetime.datetime.now()
            page.url = get_url(Page, page_name)
            page.added_by = request.user
            page.save()

            return HttpResponseRedirect(reverse('home'))


    projects = Project.objects.all()

    return render(request, 'home.html', {
        "projects": projects
    })


def login(request):
    return HttpResponseRedirect(reverse('simple-sso-login'))


@login_required
def logout(request):
    logout_user(request)
    return HttpResponseRedirect(reverse('home'))
