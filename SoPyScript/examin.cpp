#include <Inventor/nodes/SoSeparator.h>
#include <Inventor/nodes/SoTransform.h>
#include <Inventor/SoInput.h>
#include <Inventor/Qt/SoQt.h>
#include <Inventor/Qt/viewers/SoQtExaminerViewer.h>

#include "SoPyScript.h"

using namespace std;

int
main(int argc, char *argv[])
{
  if (argc != 2) {
    printf("Usage: %s file.iv\n", argv[0]);
    exit(1);
  }

  // initialize Inventor and Qt
  QWidget * w = SoQt::init(argv[0]);

  SoPyScript::initClass();

  SoInput * input = new SoInput();
  input->openFile(argv[1]);

  SoSeparator *root = new SoSeparator;
  root->ref();

  SoSeparator *vol = new SoSeparator;

  root->addChild(vol);
  root->addChild(SoDB::readAll(input));
  
  // initialize an Examiner Viewer
  SoQtExaminerViewer *myviewer = new SoQtExaminerViewer(w);
  myviewer->setSceneGraph(root);
  myviewer->show();

  SoQt::show(w);
  SoQt::mainLoop();

  return 0;
}
