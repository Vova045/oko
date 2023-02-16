from import_export import resources
from .models import Projects
 
class ProjectResource(resources.ModelResource):
    class Meta:
        model = Projects