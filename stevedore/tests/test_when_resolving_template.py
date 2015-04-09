import pytest

from resolver import TemplateResolver

template_modules = ['client_custom', 'shared', 'base']
resolve = TemplateResolver(template_modules)


def test_nonexistent_target_should_raise():
    with pytest.raises(ValueError):
        resolve('sir_not_appearing_in_this_film')


def test_should_find_file_defined_in_base():
    assert resolve('index').endswith('index.html')


def test_should_find_file_defined_in_custom():
    assert resolve('nav').endswith('nav.html')


def test_custom_file_should_override_base():
    result = resolve('nav')

    assert 'client_custom' in result
    assert 'base_app' not in result


def test_nonexistent_subpackage_target_should_raise():
    with pytest.raises(ValueError):
        resolve('admin.missing')


def test_should_find_file_defined_in_subpackage():
    assert resolve('admin.index').endswith('index.html')
