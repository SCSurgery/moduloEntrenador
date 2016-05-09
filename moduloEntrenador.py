# -*- coding: UTF-8 -*-
from __main__ import vtk, qt, ctk, slicer
import numpy,math


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

    cargarTornillosCollapsibleButton = ctk.ctkCollapsibleButton()
    cargarTornillosCollapsibleButton.text = "Cargar tornillos"
    self.layout.addWidget(cargarTornillosCollapsibleButton)
    cargarTornillosCollapsibleButton.collapsed = False

    manipulacionTornillosCollapsibleButton = ctk.ctkCollapsibleButton()
    manipulacionTornillosCollapsibleButton.text = "Manipulacion de tornillos"
    self.layout.addWidget(manipulacionTornillosCollapsibleButton)
    manipulacionTornillosCollapsibleButton.collapsed = False


#----------------------------------------------------------------------------------------------
    #Layout de planeacion:

    planeacionLayout = qt.QFormLayout(planeacionCollapsibleButton)

    insercion1Button = qt.QPushButton("Puntos de insercion") #Se crea boton pulsable, con texto "Apply"
    planeacionLayout.addWidget(insercion1Button) #Se añade el boton al layout del boton colapsable
    insercion1Button.connect('clicked(bool)',self.onApplyincersion1)

    insercion1Button = qt.QPushButton("Puntos de insercion") #Se crea boton pulsable, con texto "Apply"
    planeacionLayout.addWidget(insercion1Button) #Se añade el boton al layout del boton colapsable
    insercion1Button.connect('clicked(bool)',self.onApplyincersion1)

    reiniciarButton = qt.QPushButton("Reiniciar puntos de insercion") #Se crea boton pulsable, con texto "Apply"
    planeacionLayout.addWidget(reiniciarButton) #Se añade el boton al layout del boton colapsable
    reiniciarButton.connect('clicked(bool)',self.onApplyReiniciar)

    medirButton = qt.QPushButton("Regla") #Se crea boton pulsable, con texto "Apply"
    planeacionLayout.addWidget(medirButton) #Se añade el boton al layout del boton colapsable
    medirButton.connect('clicked(bool)',self.onApplyincersion3)

#--------------------------------------------------------------------------------------------------
    
    #Layout cargar tornillos:

    cargarTonillosLayout = qt.QFormLayout(cargarTornillosCollapsibleButton)

    cargarTonillo1 = qt.QPushButton("Cargar Tornillo 1") #Se crea boton pulsable, con texto "Apply"
    cargarTonillosLayout.addWidget(cargarTonillo1) #Se añade el boton al layout del boton colapsable
    cargarTonillo1.connect('clicked(bool)',self.onApplyCargarTornillo1)

    cargarTonillo2 = qt.QPushButton("Cargar Tornillo 2") #Se crea boton pulsable, con texto "Apply"
    cargarTonillosLayout.addWidget(cargarTonillo2) #Se añade el boton al layout del boton colapsable
    cargarTonillo2.connect('clicked(bool)',self.onApplyCargarTornillo2)

# --------------------------------------------------------------------------------------------------
  
    #Layout manipulacion de tornillos
    manipulacionLayout = qt.QFormLayout(manipulacionTornillosCollapsibleButton)

    labelSeleccionTornillo = qt.QLabel("Seleccione tornillo a mover: ") #Se crea label para seleccion de tornillo a manipular
    manipulacionLayout.addWidget(labelSeleccionTornillo) #Se añade label
 
    self.comboBoxSeleccionTornillo = qt.QComboBox() #Se crea comboBox para seleccionar tornillo
    self.comboBoxSeleccionTornillo.addItem("Tornillo 1") #Se añade opciones
    self.comboBoxSeleccionTornillo.addItem("Tornillo 2")
    manipulacionLayout.addWidget(self.comboBoxSeleccionTornillo) #Se añade al layout
   

    
    self.barraTranslacionEjeTornillo = qt.QSlider(1) #Se crea un slicer 
    self.barraTranslacionEjeTornillo.setMinimum(0) #Minimo del slider -200
    self.barraTranslacionEjeTornillo.setMaximum(50) #Maximo de slider 200
    manipulacionLayout.layout().addWidget(self.barraTranslacionEjeTornillo) #Se añade slicer al layout
    self.barraTranslacionEjeTornillo.valueChanged.connect(self.onMoveTraslacionEjeTornillo)




#---------------------------------------------------------------------------------------------------
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
    placeModePersistence = 0
    slicer.modules.markups.logic().StartPlaceMode(placeModePersistence)
    cargarTornillosCollapsibleButton.collapsed = False
    planeacionCollapsibleButton.collapsed = True

  def onApplyReiniciar(self):
    try:
        markups=slicer.util.getNode('F')
        markups.RemoveAllMarkups()
    except():
        pass
    try:
        markups2=slicer.util.getNode('G')
        markups2.RemoveAllMarkups()
    except():
        pass

  def onApplyincersion3(self):
    selectionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLSelectionNodeSingleton")
    selectionNode.SetReferenceActivePlaceNodeClassName("vtkMRMLAnnotationRulerNode")
    interactionNode = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
    placeModePersistence = 0
    interactionNode.SetPlaceModePersistence(placeModePersistence)
    interactionNode.SetCurrentInteractionMode(1)

  def onApplyCargarTornillo1(self):
    path3 = 'C:\Users\Camilo_Q\Documents\GitHub\moduloEntrenador/Tornillo_1.STL'
    slicer.util.loadModel(path3)

    referencias=slicer.util.getNode('F')
    referencias.SetNthMarkupLabel(0,"target 1")
    posicionFiducial1 = [0,0,0]
    referencias.GetNthFiducialPosition(0,posicionFiducial1)

    self.tornillo1=slicer.util.getNode('Tornillo_1') #Se obtiene la informacion del tonillo cargado
    self.transformadaTornillo1=slicer.vtkMRMLLinearTransformNode() #Se crea una transformada lineal
    self.transformadaTornillo1.SetName('Transformada Tornillo 1') #Se asigna nombre a la transformada
    slicer.mrmlScene.AddNode(self.transformadaTornillo1) #
    self.tornillo1.SetAndObserveTransformNodeID(self.transformadaTornillo1.GetID()) # Se relaciona la trnasformada con el objeto tornillo
      
    self.matriztornillo1 = vtk.vtkMatrix4x4() #Se crea matriz 4x4 para el tornillo 2
    self.transformadaTornillo1.GetMatrixTransformToParent(self.matriztornillo1) # a la matriz de tornillo 2 se toma como padre la matriz de movimiento
    self.matriztornillo1.SetElement(0,3,posicionFiducial1[0]) #Se modifica la matriz del tornillo
    self.matriztornillo1.SetElement(1,3,posicionFiducial1[1])
    self.matriztornillo1.SetElement(2,3,posicionFiducial1[2])
    self.transformadaTornillo1.SetAndObserveMatrixTransformToParent(self.matriztornillo1) # Se añade la matriz del tornillo modificada a la matriz padre de movimientos

    referencias.AddFiducial(posicionFiducial1[0],posicionFiducial1[1]-50,posicionFiducial1[2]) #Se agrega nuevo fiducial en direccion a la longitud del tornillo
    referencias.SetNthMarkupLabel(1,"access 1")

    referencias.AddObserver(referencias.PointModifiedEvent,self.onReferenciasMov)

    tornillo=slicer.util.getNode('Tornillo_1')
    tornilloModelDisplayNode = tornillo.GetDisplayNode() 
    tornilloModelDisplayNode.SetColor(1,0,0) 
    tornilloModelDisplayNode.SetSliceIntersectionVisibility(1)



  def onApplyCargarTornillo2(self):
    path4 = 'C:\Users\Camilo_Q\Documents\GitHub\moduloEntrenador/Tornillo_2.STL'
    slicer.util.loadModel(path4)

    referencias=slicer.util.getNode('F')
    posicionFiducial2 = [0,0,0]
    referencias.GetNthFiducialPosition(1,posicionFiducial2)

    referencias2 = slicer.vtkMRMLMarkupsFiducialNode()
    referencias2.SetName("G")
    slicer.mrmlScene.AddNode(referencias2)

    referencias2.AddFiducial(posicionFiducial2[0],posicionFiducial2[1],posicionFiducial2[2])
    referencias2.SetNthMarkupLabel(0,"Target 2")

    self.tornillo1=slicer.util.getNode('Tornillo_2') #Se obtiene la informacion del tonillo cargado
    self.transformadaTornillo1=slicer.vtkMRMLLinearTransformNode() #Se crea una transformada lineal
    self.transformadaTornillo1.SetName('Transformada Tornillo 2') #Se asigna nombre a la transformada
    slicer.mrmlScene.AddNode(self.transformadaTornillo1) #
    self.tornillo1.SetAndObserveTransformNodeID(self.transformadaTornillo1.GetID()) # Se relaciona la trnasformada con el objeto tornillo
      
    self.matriztornillo2 = vtk.vtkMatrix4x4() #Se crea matriz 4x4 para el tornillo 2
    self.transformadaTornillo1.GetMatrixTransformToParent(self.matriztornillo2) # a la matriz de tornillo 2 se toma como padre la matriz de movimiento
    self.matriztornillo2.SetElement(0,3,posicionFiducial2[0]) #Se modifica la matriz del tornillo
    self.matriztornillo2.SetElement(1,3,posicionFiducial2[1])
    self.matriztornillo2.SetElement(2,3,posicionFiducial2[2])
    self.transformadaTornillo1.SetAndObserveMatrixTransformToParent(self.matriztornillo2) # Se añade la matriz del tornillo modificada a la matriz padre de movimientos

    referencias2.AddFiducial(posicionFiducial2[0],posicionFiducial2[1]-50,posicionFiducial2[2]) #Se agrega nuevo fiducial en direccion a la longitud del tornillo
    referencias2.SetNthMarkupLabel(1,"access 2")

    referencias2=slicer.util.getNode('G')
    referencias2.AddObserver(referencias2.PointModifiedEvent,self.onReferenciasMov2)

    tornillo2=slicer.util.getNode('Tornillo_2')
    tornillo2ModelDisplayNode = tornillo2.GetDisplayNode() 
    tornillo2ModelDisplayNode.SetColor(0,1,0) 
    tornillo2ModelDisplayNode.SetSliceIntersectionVisibility(1)


  
  def onReferenciasMov(self,caller,event): #Se crea metodo que es llamado cuando un fiducial es desplazado por el usuario
    referencias = slicer.util.getNode("F") #Recuperamos el nodo de referencia creado
    access=numpy.array(numpy.zeros(3)) #Creamos 3 vectores vacios de 3 elemenos
    target=numpy.array(numpy.zeros(3))
    normal=numpy.array(numpy.zeros(3))
    try:
        referencias.GetNthFiducialPosition(0,target) #Se obtienen las nuevas posiciones de los fiducial y se almacenan en dos de los vectores
        referencias.GetNthFiducialPosition(1,access)
        normal=access-target # Se restan los dos puntos para obtener la direccion entre ellos
        transformadaNode=slicer.util.getNode('Transformada Tornillo 1')
        self.setTransformOrigin(target,transformadaNode) #Funcion encargada del desplazamiento
        self.setTransformNormal(normal,transformadaNode) #Funcion encargada de la rotacion
                
    except():
        pass

  def onReferenciasMov2(self,caller,event): #Se crea metodo que es llamado cuando un fiducial es desplazado por el usuario
    referencias = slicer.util.getNode("G") #Recuperamos el nodo de referencia creado
    access=numpy.array(numpy.zeros(3)) #Creamos 3 vectores vacios de 3 elemenos
    target=numpy.array(numpy.zeros(3))
    normal=numpy.array(numpy.zeros(3))
    try:
        referencias.GetNthFiducialPosition(0,target) #Se obtienen las nuevas posiciones de los fiducial y se almacenan en dos de los vectores
        referencias.GetNthFiducialPosition(1,access)
        normal=access-target # Se restan los dos puntos para obtener la direccion entre ellos
        transformadaNode=slicer.util.getNode('Transformada Tornillo 2')
        self.setTransformOrigin(target,transformadaNode) #Funcion encargada del desplazamiento
        self.setTransformNormal(normal,transformadaNode) #Funcion encargada de la rotacion

    except():
        pass 

  def setTransformOrigin(self,target,transformadaNode): #Funcion encargada del desplazamiento

    mt = vtk.vtkMatrix4x4() #Se crea nueva matriz para manipular la matriz de rot-des
    transformada=transformadaNode #Se recupera el nodo de la transformada creada
    transformada.GetMatrixTransformToParent(mt) #Se recuperan los datos actuales de la matriz padre de transformada
    mt.SetElement(0,3,target[0]) #Asigno el origen de la matriz en el fiducial target para mover el tornillo y rotar sobre este punto
    mt.SetElement(1,3,target[1])
    mt.SetElement(2,3,target[2])
    transformada.SetAndObserveMatrixTransformToParent(mt) #Se modifica la matriz rot-des de la transformada con los nuevos valores

  def setTransformNormal(self,normal,transformadaNode): #Funcion encargada de la rotacion

    vtk.vtkMath().Normalize(normal) #Se normaliza la direccion del vector entre los dos fiducial
    mt = vtk.vtkMatrix4x4()   #Se crea nueva matriz para manipular la matriz de rot-des
    transformada=transformadaNode  #Se recupera el nodo de la transformada creada
    transformada.GetMatrixTransformToParent(mt) #Se recuperan los datos actuales de la matriz padre de transformada
    cross=numpy.array(numpy.zeros(3)) #Se crea nuevo vector que contrandra el resultado de un producto cruz de 3 elementos
    #
    transform=vtk.vtkTransform() # Se crea nueva transformada 
    #
    nodeNormal=[-mt.GetElement(0,1),-mt.GetElement(1,1),-mt.GetElement(2,1)] #Recuperamos el eje z del tornillo
    nodePosicion=[mt.GetElement(0,3),mt.GetElement(1,3),mt.GetElement(2,3)] #Recuperamos la posicion del tornillo
    #
    mt.SetElement(0,3,0) #Asigno el origen de la matriz en el fiducial target para mover el tornillo y rotar sobre este punto
    mt.SetElement(1,3,0) 
    mt.SetElement(2,3,0)
    #
    vtk.vtkMath().Cross(nodeNormal,normal,cross) #Producto cruz entre el eje z y el vector dicector de los dos fiducial para calcular el vector perpendicular
    dot = vtk.vtkMath().Dot(nodeNormal,normal) #Prodducto punto entre el eje z y el vector dicector de los dos fiducial para calcular el angulo
    dot = -1.0 if (dot < -1) else (1.0 if(dot>1.0) else dot) #Operador ternario, limita a que el angulo este entre -1 y 1 ya quese aplica un coseno inverso

    #
    rotacion = vtk.vtkMath().DegreesFromRadians(math.acos(dot)) #Se calcula el angulo entre nodeNormal y normal
    #Aplicar transformada
    transform.PostMultiply() #Rota y translada en el orden correcto,"pre-multiply (or left multiply) A by B" means BA, while "post-multiply (or right multiply) A by C" means AC,Sets the internal state of the transform to PostMultiply. All subsequent operations will occur after those already represented in the current transformation. In homogeneous matrix notation, M = A*M where M is the current transformation matrix and A is the applied matrix. The default is PreMultiply.
    transform.SetMatrix(mt) #Se añade la nueva matriz que esta en el origin de coordenadas
    transform.RotateWXYZ(rotacion,cross) #Create a rotation matrix and concatenate it with the current transformation according to PreMultiply or PostMultiply semantics. The angle is in degrees, and (x,y,z) specifies the axis that the rotation will be performed around.
    transform.GetMatrix(mt) #Se recupera la matriz rotada
    #
    mt.SetElement(0,3,nodePosicion[0]) #A la nueva matriz rotada le cambio nuevamente el origen a donde estaba
    mt.SetElement(1,3,nodePosicion[1])
    mt.SetElement(2,3,nodePosicion[2])
    transformada.SetAndObserveMatrixTransformToParent(mt) # Actulizo la matriz con los cambios realizados

  def onMoveTraslacionEjeTornillo(self):
    
    valorTrasladoSlidex=self.barraTranslacionEjeTornillo.value
    print valorTrasladoSlidex
    access=numpy.array(numpy.zeros(3)) #Creamos 3 vectores vacios de 3 elemenos
    target=numpy.array(numpy.zeros(3))
    normal=numpy.array(numpy.zeros(3))
    movimientoNormal=numpy.array(numpy.zeros(3))
    try:

        if self.comboBoxSeleccionTornillo.currentIndex == 0:
            referencias = slicer.util.getNode("F")
            referencias.GetNthFiducialPosition(0,target) #Se obtienen las nuevas posiciones de los fiducial y se almacenan en dos de los vectores
            referencias.GetNthFiducialPosition(1,access)
            normal=access-target # Se restan los dos puntos para obtener la direccion entre ellos
            transformadaNode=slicer.util.getNode('Transformada Tornillo 1')
        else:
            referencias = slicer.util.getNode("G")
            referencias.GetNthFiducialPosition(0,target) #Se obtienen las nuevas posiciones de los fiducial y se almacenan en dos de los vectores
            referencias.GetNthFiducialPosition(1,access)
            normal=access-target # Se restan los dos puntos para obtener la direccion entre ellos
            transformadaNode=slicer.util.getNode('Transformada Tornillo 2')

        vtk.vtkMath().Normalize(normal) #Se normaliza la direccion del vector entre los dos fiducial
        mt = vtk.vtkMatrix4x4()   #Se crea nueva matriz para manipular la matriz de rot-des
        transformada=transformadaNode  #Se recupera el nodo de la transformada creada
        transformada.GetMatrixTransformToParent(mt)
        movimientoNormal[0]=target[0]-normal[0]*valorTrasladoSlidex
        movimientoNormal[1]=target[1]-normal[1]*valorTrasladoSlidex
        movimientoNormal[2]=target[2]-normal[2]*valorTrasladoSlidex
        mt.SetElement(0,3,movimientoNormal[0]) #Asigno el origen de la matriz en el fiducial target para mover el tornillo y rotar sobre este punto
        mt.SetElement(1,3,movimientoNormal[1])
        mt.SetElement(2,3,movimientoNormal[2])
        transformada.SetAndObserveMatrixTransformToParent(mt)
        referencias.SetNthFiducialPosition(0,movimientoNormal[0],movimientoNormal[1],movimientoNormal[2])

        
                
    except():
        pass