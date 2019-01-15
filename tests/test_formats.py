import pytest

import rbcore

# Formats tests
def test_formats_id_to_name():
    assert rbcore.utils.formats.id_to_name('this-is-slug') == 'This Is Slug'

def test_formats_get_prefixed_keys():
    set = {
        'key1': 'test',
        'toto_key2': 'test',
        'toto_key3': 'test'
    }
    result = rbcore.utils.formats.get_prefixed_keys(set, 'toto_')
    assert result.get('matching') == {
        'key2': 'test',
        'key3': 'test'
    }
    assert result.get('others') == {
        'key1': 'test'
    }
