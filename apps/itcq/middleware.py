from django.http import HttpResponse
class PrivateDraft(object):
    def process_request(self, request):
        assert hasattr(request, 'user'), "These middleware needs to go after AuthenticationMiddleware"
        if request.user.is_authenticated() or request.path.startswith("/admin/"):
            return None
        else:
            return HttpResponse("Coming soon.")
            
