import logging

from stevedore import ExtensionManager


def enumerate_template_extensions():
    # logging.basicConfig(level=logging.DEBUG)
    namespace = 'sweet_app.templates'
    manager = ExtensionManager(namespace)

    print 'Extensions in namespace {}:'.format(namespace)

    for extension in manager:
        print '\t{} (module {})'.format(extension.name,
                                        extension.entry_point.module_name)
