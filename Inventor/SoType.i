%ignore SoType::createType(const SoType parent, const SbName name,
                           const instantiationMethod method = (instantiationMethod) NULL,
                           const uint16_t data = 0);

%ignore SoType::overrideType(const SoType originalType,
                             const instantiationMethod method = (instantiationMethod) NULL);


static const SoType SoType::createType(const SoType parent, const SbName name,
                                       const instantiationMethod method = 0,
                                       const uint16_t data = 0);

static const SoType SoType::overrideType(const SoType originalType,
                                         const instantiationMethod method = 0);
