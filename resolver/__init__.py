from pkg_resources import (resource_exists as base_resource_exists,
                           resource_filename)
from stevedore import NamedExtensionManager


def resource_exists(resource_path, target):
    """Safe wrapper around pkg_resources.resource_exists

    Wrapper around pkg_resources.resource_exists that returns False instead of
    raising on ImportError

    """

    try:
        return base_resource_exists(resource_path, target)
    except ImportError:
        return False


class TemplateResolver(object):
    def __init__(self, template_modules, namespace='templates'):
        self.template_modules = template_modules
        self.extension_manager = NamedExtensionManager(namespace,
                                                       template_modules,
                                                       name_order=True)

    def __call__(self, name):
        package_suffix, target_file, join = self._process_name(name)

        for extension in self.extension_manager.extensions:
            target_package = join((extension.entry_point.module_name,
                                   package_suffix))

            if resource_exists(target_package, target_file):
                return resource_filename(target_package, target_file)
        else:
            raise ValueError(
                'Could not locate template "{}" in any loaded template '
                'module: {}'.format(name, self.template_modules))

    def _process_name(self, name):
        package_suffix, dot, basename = name.rpartition('.')
        target_file = '{}.html'.format(basename)

        if package_suffix:
            join_callable = '.'.join
        else:
            join_callable = lambda take_first: take_first[0]

        return package_suffix, target_file, join_callable
