from kajiki import PackageLoader

from resolver import TemplateResolver


class CustomPackageLoader(PackageLoader):
    def __init__(self, reload=True, force_mode=None, template_modules=None):
        super(CustomPackageLoader, self).__init__(reload=reload,
                                                  force_mode=force_mode)
        self.resolver = TemplateResolver(template_modules)

    def _filename(self, name):
        return self.resolver(name)
