package com.chinosk.uma.upd.server.Annotations;

import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)
public @interface UmaUserPermission {
    int minPermission() default 0;
}
