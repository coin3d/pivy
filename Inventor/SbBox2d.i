%extend SbBox2d {
    int __eq__(const SbBox2d & u)
    {
        return *self == u;
    };
    
    int __ne__(const SbBox2d & u)
    {
        return *self != u;
    };
}
