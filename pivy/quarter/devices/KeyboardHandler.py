/**************************************************************************\
 *
 *  This file is part of the SIM Quarter extension library for Coin.
 *  Copyright (C) 1998-2007 by Systems in Motion.  All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License ("GPL") version 2
 *  as published by the Free Software Foundation.  See the file COPYING
 *  at the root directory of this source distribution for additional
 *  information about the GNU GPL.
 *
 *  For using SIM Quarter with software that can not be combined with
 *  the GNU GPL, and for taking advantage of the additional benefits of
 *  our support services, please contact Systems in Motion about acquiring
 *  a Coin Professional Edition License.
 *
 *  See <URL:http://www.coin3d.org/> for more information.
 *
 *  Systems in Motion AS, Bygdøy allé 5, N-0257 Oslo, NORWAY. (www.sim.no)
 *
\**************************************************************************/

/*!
  \class SIM::Coin3D::Quarter::KeyboardHandler KeyboardHandler.h Quarter/devices/KeyboardHandler.h

  \brief The KeyboardHandler class provides translation of keyboard
  events on the QuarterWidget. It is registered with the DeviceManager
  by default.
*/


#include <Quarter/devices/KeyboardHandler.h>

#include <QtCore/QEvent>
#include <QtGui/QKeyEvent>
#include <Inventor/events/SoEvents.h>
#include <Inventor/events/SoKeyboardEvent.h>

#include "KeyboardHandlerP.h"

using namespace SIM::Coin3D::Quarter;

#define PRIVATE(obj) obj->pimpl

KeyboardHandler::KeyboardHandler(void)
{
  PRIVATE(this) = new KeyboardHandlerP(this);
}

KeyboardHandler::~KeyboardHandler()
{
  delete PRIVATE(this);
}

/*! Translates from QKeyEvents to SoKeyboardEvents
 */
const SoEvent *
KeyboardHandler::translateEvent(QEvent * event)
{
  switch (event->type()) {
  case QEvent::KeyPress:
  case QEvent::KeyRelease:
    return PRIVATE(this)->keyEvent((QKeyEvent *) event);
  default:
    return NULL;
  }
}

#undef PRIVATE
/**************************************************************************\
 *
 *  This file is part of the SIM Quarter extension library for Coin.
 *  Copyright (C) 1998-2007 by Systems in Motion.  All rights reserved.
 *
 *  This library is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License ("GPL") version 2
 *  as published by the Free Software Foundation.  See the file COPYING
 *  at the root directory of this source distribution for additional
 *  information about the GNU GPL.
 *
 *  For using SIM Quarter with software that can not be combined with
 *  the GNU GPL, and for taking advantage of the additional benefits of
 *  our support services, please contact Systems in Motion about acquiring
 *  a Coin Professional Edition License.
 *
 *  See <URL:http://www.coin3d.org/> for more information.
 *
 *  Systems in Motion AS, Bygdøy allé 5, N-0257 Oslo, NORWAY. (www.sim.no)
 *
\**************************************************************************/

#include "KeyboardHandlerP.h"
#include <Quarter/devices/KeyboardHandler.h>
#include <Quarter/devices/DeviceManager.h>
#include <QtCore/QMap>
#include <Inventor/errors/SoDebugError.h>

using namespace SIM::Coin3D::Quarter;

#define PUBLIC(obj) obj->publ

KeyboardHandlerP::KeyboardHandlerP(KeyboardHandler * publ)
{
  PUBLIC(this) = publ;
  this->keyboard = new SoKeyboardEvent;

  if (keyboardmap == NULL) {
    keyboardmap = new KeyMap;
    keypadmap = new KeyMap;
    this->initKeyMap();
  }
}

KeyboardHandlerP::~KeyboardHandlerP()
{
  delete this->keyboard;
}

bool
KeyboardHandlerP::debugKeyEvents(void)
{
  const char * env = coin_getenv("QUARTER_DEBUG_KEYEVENTS");
  return env && (atoi(env) > 0);
}

const SoEvent *
KeyboardHandlerP::keyEvent(QKeyEvent * qevent)
{
  const Qt::KeyboardModifiers modifiers = qevent->modifiers();

  SbVec2s pos = PUBLIC(this)->manager->getLastMousePosition();
  this->keyboard->setPosition(pos);
  PUBLIC(this)->setModifiers(this->keyboard, qevent);

  (qevent->type() == QEvent::KeyPress) ?
    this->keyboard->setState(SoButtonEvent::DOWN):
    this->keyboard->setState(SoButtonEvent::UP);

  Qt::Key qkey = (Qt::Key) qevent->key();

  SoKeyboardEvent::Key sokey = (modifiers & Qt::KeypadModifier) ?
    keypadmap->value(qkey, SoKeyboardEvent::ANY) :
    keyboardmap->value(qkey, SoKeyboardEvent::ANY);

  const char * printable = qevent->text().toAscii().constData();
  this->keyboard->setPrintableCharacter(*printable);
  this->keyboard->setKey(sokey);

#if QUARTER_DEBUG
  if (KeyboardHandlerP::debugKeyEvents()) {
    SbString s;
    this->keyboard->enumToString(this->keyboard->getKey(), s);
    SoDebugError::postInfo("KeyboardHandlerP::keyEvent",
                           "enum: '%s', pos: <%i %i>, printable: '%s'", 
                           s.getString(), 
                           pos[0], pos[1],
                           printable);
  }
#endif
  return this->keyboard;
}

KeyboardHandlerP::KeyMap * KeyboardHandlerP::keyboardmap = NULL;
KeyboardHandlerP::KeyMap * KeyboardHandlerP::keypadmap = NULL;

void
KeyboardHandlerP::initKeyMap(void)
{
  // keyboard
  keyboardmap->insert(Qt::Key_Shift,   SoKeyboardEvent::LEFT_SHIFT);
  keyboardmap->insert(Qt::Key_Alt,     SoKeyboardEvent::LEFT_ALT);
  keyboardmap->insert(Qt::Key_Control, SoKeyboardEvent::LEFT_CONTROL);
  keyboardmap->insert(Qt::Key_0, SoKeyboardEvent::NUMBER_0);
  keyboardmap->insert(Qt::Key_1, SoKeyboardEvent::NUMBER_1);
  keyboardmap->insert(Qt::Key_2, SoKeyboardEvent::NUMBER_2);
  keyboardmap->insert(Qt::Key_3, SoKeyboardEvent::NUMBER_3);
  keyboardmap->insert(Qt::Key_4, SoKeyboardEvent::NUMBER_4);
  keyboardmap->insert(Qt::Key_5, SoKeyboardEvent::NUMBER_5);
  keyboardmap->insert(Qt::Key_6, SoKeyboardEvent::NUMBER_6);
  keyboardmap->insert(Qt::Key_7, SoKeyboardEvent::NUMBER_7);
  keyboardmap->insert(Qt::Key_8, SoKeyboardEvent::NUMBER_8);
  keyboardmap->insert(Qt::Key_9, SoKeyboardEvent::NUMBER_9);

  keyboardmap->insert(Qt::Key_A, SoKeyboardEvent::A);
  keyboardmap->insert(Qt::Key_B, SoKeyboardEvent::B);
  keyboardmap->insert(Qt::Key_C, SoKeyboardEvent::C);
  keyboardmap->insert(Qt::Key_D, SoKeyboardEvent::D);
  keyboardmap->insert(Qt::Key_E, SoKeyboardEvent::E);
  keyboardmap->insert(Qt::Key_F, SoKeyboardEvent::F);
  keyboardmap->insert(Qt::Key_G, SoKeyboardEvent::G);
  keyboardmap->insert(Qt::Key_H, SoKeyboardEvent::H);
  keyboardmap->insert(Qt::Key_I, SoKeyboardEvent::I);
  keyboardmap->insert(Qt::Key_J, SoKeyboardEvent::J);
  keyboardmap->insert(Qt::Key_K, SoKeyboardEvent::K);
  keyboardmap->insert(Qt::Key_L, SoKeyboardEvent::L);
  keyboardmap->insert(Qt::Key_M, SoKeyboardEvent::M);
  keyboardmap->insert(Qt::Key_N, SoKeyboardEvent::N);
  keyboardmap->insert(Qt::Key_O, SoKeyboardEvent::O);
  keyboardmap->insert(Qt::Key_P, SoKeyboardEvent::P);
  keyboardmap->insert(Qt::Key_Q, SoKeyboardEvent::Q);
  keyboardmap->insert(Qt::Key_R, SoKeyboardEvent::R);
  keyboardmap->insert(Qt::Key_S, SoKeyboardEvent::S);
  keyboardmap->insert(Qt::Key_T, SoKeyboardEvent::T);
  keyboardmap->insert(Qt::Key_U, SoKeyboardEvent::U);
  keyboardmap->insert(Qt::Key_V, SoKeyboardEvent::V);
  keyboardmap->insert(Qt::Key_W, SoKeyboardEvent::W);
  keyboardmap->insert(Qt::Key_X, SoKeyboardEvent::X);
  keyboardmap->insert(Qt::Key_Y, SoKeyboardEvent::Y);
  keyboardmap->insert(Qt::Key_Z, SoKeyboardEvent::Z);

  keyboardmap->insert(Qt::Key_Home,     SoKeyboardEvent::HOME);
  keyboardmap->insert(Qt::Key_Left,     SoKeyboardEvent::LEFT_ARROW);
  keyboardmap->insert(Qt::Key_Up,       SoKeyboardEvent::UP_ARROW);
  keyboardmap->insert(Qt::Key_Right,    SoKeyboardEvent::RIGHT_ARROW);
  keyboardmap->insert(Qt::Key_Down,     SoKeyboardEvent::DOWN_ARROW);
  keyboardmap->insert(Qt::Key_PageUp,   SoKeyboardEvent::PAGE_UP);
  keyboardmap->insert(Qt::Key_PageDown, SoKeyboardEvent::PAGE_DOWN);
  keyboardmap->insert(Qt::Key_End,      SoKeyboardEvent::END);

  keyboardmap->insert(Qt::Key_F1,  SoKeyboardEvent::F1);
  keyboardmap->insert(Qt::Key_F2,  SoKeyboardEvent::F2);
  keyboardmap->insert(Qt::Key_F3,  SoKeyboardEvent::F3);
  keyboardmap->insert(Qt::Key_F4,  SoKeyboardEvent::F4);
  keyboardmap->insert(Qt::Key_F5,  SoKeyboardEvent::F5);
  keyboardmap->insert(Qt::Key_F6,  SoKeyboardEvent::F6);
  keyboardmap->insert(Qt::Key_F7,  SoKeyboardEvent::F7);
  keyboardmap->insert(Qt::Key_F8,  SoKeyboardEvent::F8);
  keyboardmap->insert(Qt::Key_F9,  SoKeyboardEvent::F9);
  keyboardmap->insert(Qt::Key_F10, SoKeyboardEvent::F10);
  keyboardmap->insert(Qt::Key_F11, SoKeyboardEvent::F11);
  keyboardmap->insert(Qt::Key_F12, SoKeyboardEvent::F12);

  keyboardmap->insert(Qt::Key_Backspace,  SoKeyboardEvent::BACKSPACE);
  keyboardmap->insert(Qt::Key_Tab,        SoKeyboardEvent::TAB);
  keyboardmap->insert(Qt::Key_Return,     SoKeyboardEvent::RETURN);
  keyboardmap->insert(Qt::Key_Enter,      SoKeyboardEvent::ENTER);
  keyboardmap->insert(Qt::Key_Pause,      SoKeyboardEvent::PAUSE);
  keyboardmap->insert(Qt::Key_ScrollLock, SoKeyboardEvent::SCROLL_LOCK);
  keyboardmap->insert(Qt::Key_Escape,     SoKeyboardEvent::ESCAPE);
  keyboardmap->insert(Qt::Key_Delete,     SoKeyboardEvent::DELETE);
  keyboardmap->insert(Qt::Key_Print,      SoKeyboardEvent::PRINT);
  keyboardmap->insert(Qt::Key_Insert,     SoKeyboardEvent::INSERT);
  keyboardmap->insert(Qt::Key_NumLock,    SoKeyboardEvent::NUM_LOCK);
  keyboardmap->insert(Qt::Key_CapsLock,   SoKeyboardEvent::CAPS_LOCK);

  keyboardmap->insert(Qt::Key_Space,        SoKeyboardEvent::SPACE);
  keyboardmap->insert(Qt::Key_Apostrophe,   SoKeyboardEvent::APOSTROPHE);
  keyboardmap->insert(Qt::Key_Comma,        SoKeyboardEvent::COMMA);
  keyboardmap->insert(Qt::Key_Minus,        SoKeyboardEvent::MINUS);
  keyboardmap->insert(Qt::Key_Period,       SoKeyboardEvent::PERIOD);
  keyboardmap->insert(Qt::Key_Slash,        SoKeyboardEvent::SLASH);
  keyboardmap->insert(Qt::Key_Semicolon,    SoKeyboardEvent::SEMICOLON);
  keyboardmap->insert(Qt::Key_Equal,        SoKeyboardEvent::EQUAL);
  keyboardmap->insert(Qt::Key_BracketLeft,  SoKeyboardEvent::BRACKETLEFT);
  keyboardmap->insert(Qt::Key_BracketRight, SoKeyboardEvent::BRACKETRIGHT);
  keyboardmap->insert(Qt::Key_Backslash,    SoKeyboardEvent::BACKSLASH);
  keyboardmap->insert(Qt::Key_Agrave,       SoKeyboardEvent::GRAVE);

  // keypad

  // on Mac OS X, the keypad modifier will also be set when an arrow
  // key is pressed as the arrow keys are considered part of the
  // keypad
  keypadmap->insert(Qt::Key_Left,     SoKeyboardEvent::LEFT_ARROW);
  keypadmap->insert(Qt::Key_Up,       SoKeyboardEvent::UP_ARROW);
  keypadmap->insert(Qt::Key_Right,    SoKeyboardEvent::RIGHT_ARROW);
  keypadmap->insert(Qt::Key_Down,     SoKeyboardEvent::DOWN_ARROW);

  keypadmap->insert(Qt::Key_Enter,    SoKeyboardEvent::PAD_ENTER);
  keypadmap->insert(Qt::Key_F1,       SoKeyboardEvent::PAD_F1);
  keypadmap->insert(Qt::Key_F2,       SoKeyboardEvent::PAD_F2);
  keypadmap->insert(Qt::Key_F3,       SoKeyboardEvent::PAD_F3);
  keypadmap->insert(Qt::Key_F4,       SoKeyboardEvent::PAD_F4);
  keypadmap->insert(Qt::Key_0,        SoKeyboardEvent::PAD_0);
  keypadmap->insert(Qt::Key_1,        SoKeyboardEvent::PAD_1);
  keypadmap->insert(Qt::Key_2,        SoKeyboardEvent::PAD_2);
  keypadmap->insert(Qt::Key_3,        SoKeyboardEvent::PAD_3);
  keypadmap->insert(Qt::Key_4,        SoKeyboardEvent::PAD_4);
  keypadmap->insert(Qt::Key_5,        SoKeyboardEvent::PAD_5);
  keypadmap->insert(Qt::Key_6,        SoKeyboardEvent::PAD_6);
  keypadmap->insert(Qt::Key_7,        SoKeyboardEvent::PAD_7);
  keypadmap->insert(Qt::Key_8,        SoKeyboardEvent::PAD_8);
  keypadmap->insert(Qt::Key_9,        SoKeyboardEvent::PAD_9);
  keypadmap->insert(Qt::Key_Plus,     SoKeyboardEvent::PAD_ADD);
  keypadmap->insert(Qt::Key_Minus,    SoKeyboardEvent::PAD_SUBTRACT);
  keypadmap->insert(Qt::Key_multiply, SoKeyboardEvent::PAD_MULTIPLY);
  keypadmap->insert(Qt::Key_division, SoKeyboardEvent::PAD_DIVIDE);
  keypadmap->insert(Qt::Key_Tab,      SoKeyboardEvent::PAD_TAB);
  keypadmap->insert(Qt::Key_Space,    SoKeyboardEvent::PAD_SPACE);
  keypadmap->insert(Qt::Key_Insert,   SoKeyboardEvent::PAD_INSERT);
  keypadmap->insert(Qt::Key_Delete,   SoKeyboardEvent::PAD_DELETE);
  keypadmap->insert(Qt::Key_Period,   SoKeyboardEvent::PAD_PERIOD);


#if 0 // FIXME: don't know what to do with these (20070306 frodo)
  keyboardmap->insert(Qt::, SoKeyboardEvent::RIGHT_SHIFT);
  keyboardmap->insert(Qt::, SoKeyboardEvent::RIGHT_CONTROL);
  keyboardmap->insert(Qt::, SoKeyboardEvent::RIGHT_ALT);
  keyboardmap->insert(Qt::, SoKeyboardEvent::PRIOR);
  keyboardmap->insert(Qt::, SoKeyboardEvent::NEXT);
  keyboardmap->insert(Qt::, SoKeyboardEvent::SHIFT_LOCK);
#endif
}

#undef PUBLIC
