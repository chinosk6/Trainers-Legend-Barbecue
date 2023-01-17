package com.chinosk.uma.upd.server.processor;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.io.FileInputStream;
import java.math.BigInteger;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import static com.chinosk.uma.upd.server.processor.FileController.transFileBasePath;

public class BaseTools {

    public static String getFileMd5(File file) {
            try (FileInputStream fis = new FileInputStream(file)) {
            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] buffer = new byte[1024];
            int length = -1;
            while ((length = fis.read(buffer, 0, 1024)) != -1) {
                md.update(buffer, 0, length);
            }
            BigInteger bigInt = new BigInteger(1, md.digest());
            return bigInt.toString(16);
        }
        catch (Exception ex) {
            Logger logger = LoggerFactory.getLogger(BaseTools.class);
            logger.error("Exception occurred in getFileMd5: " + ex);
            return null;
        }
    }

    public static String getRandomString(int length){
        String str="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        Random random=new Random();
        StringBuilder ret=new StringBuilder();
        for(int i=0; i<length; i++){
            int number=random.nextInt(62);
            ret.append(str.charAt(number));
        }
        return ret.toString();
    }

    public static String getFileRelativePath(File file) {
        String fullPath = file.getPath().replace("\\", "/");
        String basePath = transFileBasePath.replace("\\", "/");
        return fullPath.replace(basePath, "");
    }

    public static class GetAllFileFromPath {
        File basePath;
        List<File> ret = new ArrayList<>();

        public GetAllFileFromPath(String filePath) {
            basePath = new File(filePath);
        }
        public GetAllFileFromPath(File filePath) {
            basePath = filePath;
        }

        public void getAllFilePath(File srcFile) {
            File[] fileArray = srcFile.listFiles();
            if (fileArray != null) {
                for (File file : fileArray){
                    if(file.isDirectory()){
                        getAllFilePath(file);
                    }
                    else {
                        ret.add(file.getAbsoluteFile());
                    }
                }
            }
        }

        public List<File> getResult() {
            getAllFilePath(basePath);
            return ret;
        }
    }

}
