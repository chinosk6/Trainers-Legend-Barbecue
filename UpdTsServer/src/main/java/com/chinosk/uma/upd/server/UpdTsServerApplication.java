package com.chinosk.uma.upd.server;

import com.chinosk.uma.upd.server.dbaccessobj.UmaUsersDAO;
import com.chinosk.uma.upd.server.processor.FileController;
import org.mybatis.spring.annotation.MapperScan;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.event.ApplicationStartedEvent;
import org.springframework.context.ApplicationListener;
import org.springframework.stereotype.Component;

import java.util.Map;

@SpringBootApplication
@MapperScan("com.chinosk.uma.upd.server.mapper")
public class UpdTsServerApplication {
    public static boolean isCreateUser = false;
    public static String createUserName = null;

    public static void main(String[] args) {
        for (String i : args) {
            if (i.startsWith("--createuser")) {
                isCreateUser = true;
                createUserName = i.substring(13).strip();
            }
        }

        SpringApplication.run(UpdTsServerApplication.class, args);
    }
}


@Component
class StartInit implements ApplicationListener<ApplicationStartedEvent> {
    public static Logger logger = LoggerFactory.getLogger(ApplicationListener.class);
    @Override
    public void onApplicationEvent(ApplicationStartedEvent event) {
        com.chinosk.uma.upd.server.processor.FileController.FileSync();
        if (UpdTsServerApplication.isCreateUser) {
            String userName = UpdTsServerApplication.createUserName;
            Map<String, Object> addUser = UmaUsersDAO.getInstance().addUser(userName, UmaUsersDAO.OWNER);
            logger.info("Create user: " + addUser);
        }


    }
}
