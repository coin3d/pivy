%ignore SoType::createType(const SoType parent, const SbName name,
                           const instantiationMethod method = (instantiationMethod) NULL,
                           const uint16_t data = 0);

%ignore SoType::overrideType(const SoType originalType,
                             const instantiationMethod method = (instantiationMethod) NULL);

/* autocast the result of createInstace to the corresponding type */
%extend SoType {
  PyObject * createInstance(void) {
    if (self->isDerivedFrom(SoField::getClassTypeId())) {
      return autocast_field((SoField*)self->createInstance());
    } else if (self->isDerivedFrom(SoField::getClassTypeId())) {
      return autocast_path((SoPath*)self->createInstance());
    }
    return autocast_base((SoBase*)self->createInstance());
  }
}

static const SoType SoType::createType(const SoType parent, const SbName name,
                                       const instantiationMethod method = 0,
                                       const uint16_t data = 0);

static const SoType SoType::overrideType(const SoType originalType,
                                         const instantiationMethod method = 0);
