class ContextMiddleware:

    @staticmethod
    def validate(context):
        if not isinstance(context, dict):
            raise ValueError("Context must be a dictionary.")
        return context
