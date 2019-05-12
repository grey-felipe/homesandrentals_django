import json
from rest_framework.renderers import JSONRenderer


class PropertyRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        errors = data.get('errors', None)

        if errors is not None:
            return super(PropertyRenderer, self).render(data)

        return json.dumps({'property': data})


class PropertyListRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return json.dumps({'property': data})
