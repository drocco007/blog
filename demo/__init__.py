import logging

from stevedore import ExtensionManager


def enumerate_template_extensions():
    logging.basicConfig(level=logging.DEBUG)
    manager = ExtensionManager('templates')

    print 'Extensions in namespace "templates":'

    for extension in manager:
        print '\t{} (module {})'.format(extension.name,
                                        extension.entry_point.module_name)
