from rest_framework.response import Response

class ApiResponseMixin:
    def api_response(self, success=True, message="", data=None, status_code=200):
        return Response({
            "success": success,
            "message": message,
            "data": data
        }, status=status_code)


    def get_bool_param(self,request, key, default=False):
        val = request.GET.get(key)
        if val is None:
            return default
        return str(val).strip().lower() in ['1', 'true', 'yes', 'on', '']
