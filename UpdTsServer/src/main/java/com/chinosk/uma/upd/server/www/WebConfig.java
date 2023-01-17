package com.chinosk.uma.upd.server.www;

import com.chinosk.uma.upd.server.www.interceptor.MainInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new MainInterceptor())
                .addPathPatterns("/api/*")
                //.excludePathPatterns("/login")
        ;

    }

}
