#define OF_PROPERTY_READ(type, np, propname, out) ({                \
    int __ret = -EINVAL;                                            \
    if ((type) == u32)                                              \
        __ret = of_property_read_u32((np), (propname), (out));      \
    else if ((type) == u16)                                         \
        __ret = of_property_read_u16((np), (propname), (out));      \
    else if ((type) == bool) {                                      \
        *(out) = of_property_read_bool((np), (propname));           \
        __ret = 0;                                                  \
    }                                                               \
    if (__ret == 0) {                                               \
        if ((type) == bool)                                         \
            pr_info("Device Tree: Found property '%s', value: %s\n",\
                    (propname), *(out) ? "true" : "false");         \
        else                                                        \
            pr_info("Device Tree: Found property '%s', value: %u\n",\
                    (propname), (unsigned int)(*(out)));            \
    } else {                                                        \
        pr_err("Device Tree: Property '%s' not found\n", (propname)); \
    }                                                               \
    __ret;                                                          \
})
