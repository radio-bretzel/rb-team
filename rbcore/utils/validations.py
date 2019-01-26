import re, html
from cerberus import Validator

from .errors import ValidationError

def validate(data, schema, mandatories=True, allow_unknown=False, **kwargs):
    """ Validate given data with given Schema. kwargs are passed to cerberus.Validator consructor """
    v = RB_Validator(schema=schema, allow_unknown=allow_unknown, **kwargs)
    update = not mandatories
    valids = v.validated(data, update=update)
    if valids is None:
        raise ValidationError(v.errors)
    return valids


class RB_Validator(Validator):

    def _normalize_coerce_text(self, value):
        return html.escape(value)

    def _normalize_coerce_boolean(self, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            if value.lower() == 'true': return True
            if value.lower() == 'false': return False
            return value


    def _validator_boolean(self, field, value):
        if not isinstance(value, bool):
            self._error(field, "Must be boolean")

    def _validator_uuid(self, field, value):
        if not re.match('^[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$', value, re.IGNORECASE):
            self._error(field, "Must be valid UUID")

    def _validator_slug(self, field, value):
        if not re.match('^([a-z][a-z0-9]*)((?:-[a-z0-9]+){0,2})$', value):
            self._error(field, 'Must be only letters, digits and maximum two dashes. Cannot start nor end with a dash.')

    def _validator_url(self, field, value):
        if not re.match('^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$', value):
            self._error(field, "Must be a valid url")
