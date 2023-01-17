package com.chinosk.uma.upd.server.www.interceptor;

import com.chinosk.uma.upd.server.dbaccessobj.FileInfoDAO;
import com.chinosk.uma.upd.server.processor.FileController;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.HashMap;
import java.util.Map;

import static com.chinosk.uma.upd.server.www.MainController.returnGenerator;

@ControllerAdvice
public class ErrorHandler {

    public static Logger logger = LoggerFactory.getLogger(ErrorHandler.class);

    @ExceptionHandler(Exception.class)
    @ResponseBody
    public ResponseEntity<HashMap<String, Object>> baseExRet(Exception ex) {
        logger.error("Exception Occurred: " + ex);
        ex.printStackTrace();
        return returnGenerator(500, false, "Internal Server Error", null);
    }
}
