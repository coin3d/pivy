// SPDX-License-Identifier: ISC

%extend SoSFPath {
  void setValue(const SoSFPath * other) { *self = *other; }
}
