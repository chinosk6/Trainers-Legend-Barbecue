package com.chinosk.uma.upd.server;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.event.ApplicationStartedEvent;
import org.springframework.context.ApplicationListener;
import org.springframework.stereotype.Component;

@SpringBootApplication
@MapperScan("com.chinosk.uma.upd.server.mapper")
public class UpdTsServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(UpdTsServerApplication.class, args);
    }
}


@Component
class StartInit implements ApplicationListener<ApplicationStartedEvent> {
    @Override
    public void onApplicationEvent(ApplicationStartedEvent event) {
        com.chinosk.uma.upd.server.processor.FileController.FileSync();
    }
}

