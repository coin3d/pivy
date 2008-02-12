#ifndef mainwindow_h_
#define mainwindow_h_

#include <QMainWindow>
#include "ui_test.h"

class MainWindow : public QMainWindow, public Ui::MainWindow
{
  Q_OBJECT;

  class SoQtExaminerViewer *exam;
  void setupSoQt();
 public:
  MainWindow(QWidget *parent = 0);
};

#endif
