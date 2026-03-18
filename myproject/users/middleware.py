class DebugAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Before view
        print("Session Key:", request.session.session_key)
        print("User before view:", getattr(request, "user", None))

        response = self.get_response(request)

        # After view
        print("User after view:", getattr(request, "user", None))

        return response