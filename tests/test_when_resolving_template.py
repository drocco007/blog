import pytest

from resolver import template


def test_nonexistent_target_should_raise():
    with pytest.raises(ValueError):
        template('sir_not_appearing_in_this_film')


def test_should_find_file_defined_in_base():
    assert template('index').endswith('index.html')


def test_should_find_file_defined_in_custom():
    assert template('nav').endswith('nav.html')


def test_custom_file_should_override_base():
    result = template('nav')

    assert 'client_custom' in result
    assert 'base_app' not in result


def test_nonexistent_subpackage_target_should_raise():
    with pytest.raises(ValueError):
        template('admin.missing')


def test_should_find_file_defined_in_subpackage():
    assert template('admin.index').endswith('index.html')
