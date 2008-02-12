#include <QApplication>
#include "mainwindow.h"
#include <Inventor/Qt/SoQt.h>

int main(int argc, char *argv[])
{
  SoQt::init(argc, argv, argv[0]);
  QApplication app(argc, argv);
  MainWindow *mw = new MainWindow();
  mw->show();
  return app.exec();
}
