#include "mainwindow.h"
#include <Inventor/nodes/SoSeparator.h>
#include <Inventor/nodes/SoRotationXYZ.h>
#include <Inventor/nodes/SoMaterial.h>
#include <Inventor/nodes/SoCone.h>
#include <Inventor/engines/SoGate.h>
#include <Inventor/engines/SoElapsedTime.h>
#include <Inventor/fields/SoMFFloat.h>
#include <Inventor/Qt/viewers/SoQtExaminerViewer.h>

MainWindow::MainWindow(QWidget *parent)
  :QMainWindow(parent)
{
  setupUi(this);
  setupSoQt();
}

void
MainWindow::setupSoQt()
{
  SoSeparator *root = new SoSeparator();
  SoRotationXYZ *rotxyz = new SoRotationXYZ();
  SoGate *gate = new SoGate(SoMFFloat::getClassTypeId());
  SoElapsedTime *elapsedTime = new SoElapsedTime();
  gate->enable = false;
  gate->input->connectFrom(&elapsedTime->timeOut);
  rotxyz->angle.connectFrom(gate->output);
  SoMaterial *material = new SoMaterial();
  material->diffuseColor = SbColor(0.0, 1.0, 1.0);
  SoCone *cone = new SoCone();
  root->addChild(rotxyz);
  root->addChild(material);
  root->addChild(cone);
    
  this->exam = new SoQtExaminerViewer(this->examiner);
  this->exam->setSceneGraph(root);
}
