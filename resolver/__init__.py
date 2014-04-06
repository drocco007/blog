from pkg_resources import (resource_exists as base_resource_exists,
                           resource_filename)
from stevedore import NamedExtensionManager


template_modules = ['client_custom', 'shared', 'base']

extension_manager = NamedExtensionManager('templates', template_modules,
                                          name_order=True)


def resource_exists(resource_path, target):
    """Safe wrapper around pkg_resources.resource_exists

    Wrapper around pkg_resources.resource_exists that returns False instead of
    raising on ImportError

    """

    try:
        return base_resource_exists(resource_path, target)
    except ImportError:
        return False


def template(name):
    package_suffix, dot, basename = name.rpartition('.')
    target_file = '{}.html'.format(basename)

    if package_suffix:
        join = '.'.join
    else:
        join = lambda take_first: take_first[0]

    for extension in extension_manager.extensions:
        target_package = join((extension.entry_point.module_name,
                               package_suffix))

        if resource_exists(target_package, target_file):
            return resource_filename(target_package, target_file)
    else:
        raise ValueError(
            'Could not locate template {} in any loaded template module: {}'
            .format(name, template_modules))
