import pytest
from rbcore.utils import validations
from rbcore.errors import ValidationError

def test_RB_Validator_normalizator():
    validator = validations.RB_Validator()
    assert validator._normalize_coerce_text('<html>Test Text</html>') == '&lt;html&gt;Test Text&lt;/html&gt;'
    assert validator._normalize_coerce_boolean('true') == True
    assert validator._normalize_coerce_boolean(True) == True

def test_validate():
    test_schema = {
        'uuid': {
            'validator': 'uuid'
        },
        'slug': {
            'validator': 'slug'
        },
        'url': {
            'validator': 'url'
        },
        'text': {
            'coerce': 'text'
        },
        'bool': {
            'validator': 'boolean',
            'coerce': 'boolean'
        }
    }

    test_dataset_1 = {
        'uuid': "3d2d85ba-b7da-462d-989a-d3edc70454af",
        'slug': "radio-bretzel",
        'url': "https://radio-bretzel.io",
        'text': '<html>Test Text</html>',
        'bool': 'true'
    }
    test_dataset_2 = {
        'url': 'radio-bretzel.io',
        'bool': True
    }
    test_empty_dataset = {}

    assert validations.validate(test_dataset_1, test_schema)
    assert validations.validate(test_dataset_2, test_schema)
    assert validations.validate(test_empty_dataset, test_schema) == {}
