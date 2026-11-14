// SPDX-License-Identifier: ISC

%extend SoSFFloat {
  void setValue(const SoSFFloat * other) { *self = *other; }
}
