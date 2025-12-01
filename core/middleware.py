from django.template import TemplateDoesNotExist
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
import os


class TemplateAutoCreateMiddleware(MiddlewareMixin):
    """
    Middleware that creates basic templates on-the-fly when they don't exist
    """
    
    def process_exception(self, request, exception):
        if isinstance(exception, TemplateDoesNotExist):
            # Get the missing template name
            template_name = str(exception.args[0]) if exception.args else None
            
            if template_name:
                # Return a generic fallback template
                return render(request, 'base/generic_fallback.html', {
                    'missing_template': template_name,
                    'request_path': request.path,
                    'message': f'Template "{template_name}" not found. Using fallback.'
                }, status=200)
        
        return None