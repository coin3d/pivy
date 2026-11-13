// SPDX-License-Identifier: ISC

%extend SoSFBool {
  void setValue(const SoSFBool * other) { *self = *other; }
}
