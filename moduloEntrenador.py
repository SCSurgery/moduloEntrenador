from __main__ import vtk, qt, ctk, slicer


class moduloEntrenador:
  def __init__(self, parent):
    parent.title = "Modulo Entrenador"
    parent.categories = ["Ejemplos"]
    parent.dependencies = []
    parent.contributors = ["Camilo Quiceno Q"] 
    parent.helpText = """
    Este modulo sirve para simular la fijacion de tornillos transpediculares
    """
    parent.acknowledgementText = """
    Desarrollado por Camilo Quiceno 
    """ 
    self.parent = parent



class moduloEntrenadorWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):

    sampleCollapsibleButton = ctk.ctkCollapsibleButton()
    sampleCollapsibleButton.text = "A collapsible button"
    self.layout.addWidget(sampleCollapsibleButton)

    
    sampleFormLayout = qt.QFormLayout(sampleCollapsibleButton)



