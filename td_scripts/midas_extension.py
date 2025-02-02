class MidasExt:
    def __init__(self, ownerComp):
        self.ownerComp = ownerComp

    def Installdep(self):
        text_template = self.ownerComp.op('text_template')
        if text_template:
            text_template.run()

    def Runpaths(self):

        text_paths = self.ownerComp.op('text_paths')
        if text_paths:
            text_paths.run()

    def Loadmidasmodel(self):
        midas_loader = self.ownerComp.op('midas_loader')
        if midas_loader:
            midas_loader.run()
