%extend SoNodeKitPath {      
    int __eq__( const SoNodeKitPath &u )
    {
        return *self == u;
    };
    
    int __nq__( const SoNodeKitPath &u )
    {
        return !(*self == u);
    };
}
