// SPDX-License-Identifier: ISC

%extend SoSFPlane {
  void setValue(const SoSFPlane * other) { *self = *other; }
}
