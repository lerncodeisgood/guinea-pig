from rest_framework import renderers


class CentralizedResponseRenderer(renderers.JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = data or {}
        return super().render({**response_data})
