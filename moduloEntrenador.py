# -*- coding: UTF-8 -*-
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

    self.cargarScene()

    #Definicion botenes colapsables:
#--------------------------------------------------------------------------------------------------
    planeacionCollapsibleButton = ctk.ctkCollapsibleButton()
    planeacionCollapsibleButton.text = "Planeacion"
    self.layout.addWidget(planeacionCollapsibleButton)

    #Layout de planeacion:

    planeacionLayout = qt.QFormLayout(planeacionCollapsibleButton)

    insercion1Button = qt.QPushButton("Puntos de insercion") #Se crea boton pulsable, con texto "Apply"
    planeacionLayout.addWidget(insercion1Button) #Se añade el boton al layout del boton colapsable
    insercion1Button.connect('clicked(bool)',self.onApplyincersion1)

    insercion2Button = qt.QPushButton("Reiniciar puntos de insercion") #Se crea boton pulsable, con texto "Apply"
    planeacionLayout.addWidget(insercion2Button) #Se añade el boton al layout del boton colapsable
    insercion2Button.connect('clicked(bool)',self.onApplyincersion2)

    medirButton = qt.QPushButton("Regla") #Se crea boton pulsable, con texto "Apply"
    planeacionLayout.addWidget(medirButton) #Se añade el boton al layout del boton colapsable
    medirButton.connect('clicked(bool)',self.onApplyincersion3)

#--------------------------------------------------------------------------------------------------
  def cargarScene(self):

    path1='C:\Users\Camilo_Q\Documents\GitHub\moduloEntrenador/stlcolumna.stl' #Se obtiene direccion de la unbicación del tornillo
    path2='C:\Users\Camilo_Q\Documents\GitHub\moduloEntrenador\Lumbar 2.5 B31s - 4/4 Lumbar  2.5  B31s.nrrd'
    slicer.util.loadModel(path1)
    slicer.util.loadVolume(path2)

    columna=slicer.util.getNode('stlcolumna') # Se obtiene el nodo del objeto en escena
    columnaModelDisplayNode = columna.GetDisplayNode() 
    columnaModelDisplayNode.SetColor(1,1,3) 
    columnaModelDisplayNode.SetSliceIntersectionVisibility(1)
    transformadaColumna=slicer.vtkMRMLLinearTransformNode()
    transformadaColumna.SetName('Transformada')
    slicer.mrmlScene.AddNode(transformadaColumna)
    columna.SetAndObserveTransformNodeID(transformadaColumna.GetID()) #Asocia el objeto a la matriz
    mt = vtk.vtkMatrix4x4()
    transformadaColumna.GetMatrixTransformToParent(mt)
    mt.SetElement(0,0,-1) #Asigno el origen de la matriz en el fiducial target para mover el tornillo y rotar sobre este punto
    mt.SetElement(1,1,-1)
    transformadaColumna.SetAndObserveMatrixTransformToParent(mt)
    layoutManager = slicer.app.layoutManager() 
    threeDWidget = layoutManager.threeDWidget(0)
    threeDView = threeDWidget.threeDView()
    threeDView.resetFocalPoint()

  def onApplyincersion1(self):
    placeModePersistence = 0
    slicer.modules.markups.logic().StartPlaceMode(placeModePersistence)

  def onApplyincersion2(self):
    markups=slicer.util.getNode('F')
    markups.RemoveAllMarkups()

  def onApplyincersion3(self):
    selectionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSelectionNodeSingleton")
    selectionNode.SetReferenceActivePlaceNodeClassName("vtkMRMLAnnotationRulerNode")
    interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
    placeModePersistence = 0
    interactionNode.SetPlaceModePersistence(placeModePersistence)
    interactionNode.SetCurrentInteractionMode(1)



