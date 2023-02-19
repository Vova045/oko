from AppOko.models import Projects

def get_projects(request):
    projects=Projects.objects.all()
    my_host=request.get_host()
    return {
        'projects': projects,
        'my_host': my_host
    }