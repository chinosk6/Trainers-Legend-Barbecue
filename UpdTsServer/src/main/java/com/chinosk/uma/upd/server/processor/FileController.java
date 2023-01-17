package com.chinosk.uma.upd.server.processor;

import com.chinosk.uma.upd.server.dbaccessobj.FileInfoDAO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.util.List;

public class FileController {
    public static final String transFileBasePath = System.getProperty("user.dir") + "/trans_files";
    public static Logger logger = LoggerFactory.getLogger(FileController.class);

    public static void FileSync() {
        logger.info("Sync files...");
        List<File> allFiles = new BaseTools.GetAllFileFromPath(transFileBasePath).getResult();
        if (allFiles == null){
            return;
        }
        FileInfoDAO fileController = FileInfoDAO.getInstance();
        for (File i : allFiles) {
            fileController.insertOrUpdateFileInfo(i, 0, null);
        }
        fileController.syncDeleteFileInDb(allFiles);
        logger.info("Sync finished.");
    }

    public static boolean deleteLocalFile(String filename) {
        String basePath = transFileBasePath.replace("\\", "/");
        String fileFullPath = basePath + "/" + filename;
        File file = new File(fileFullPath);
        if (!file.exists()) {
            return false;
        }
        return file.delete();
    }

}
