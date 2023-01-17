package com.chinosk.uma.upd.server.dbaccessobj;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.chinosk.uma.upd.server.mapper.FileInfoMapper;
import com.chinosk.uma.upd.server.models.FileInfoBase;
import com.chinosk.uma.upd.server.processor.BaseTools;
import com.chinosk.uma.upd.server.processor.FileController;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

@Component
public class FileInfoDAO {
    private final FileInfoMapper fileMapper;
    public static FileInfoDAO fileInfoDAO;
    public static Logger logger = LoggerFactory.getLogger(FileInfoDAO.class);

    @Autowired
    public FileInfoDAO(FileInfoMapper fileMapper) {
        MapperSaver.setFileInfoMapper(fileMapper);
        this.fileMapper = fileMapper;
        fileInfoDAO = this;
    }

    public FileInfoDAO() {
        this.fileMapper = MapperSaver.getFileInfoMapper();
        fileInfoDAO = this;
    }

    public static FileInfoDAO getInstance() {
        if (fileInfoDAO == null) {
            new FileInfoDAO();
        }
        return fileInfoDAO;
    }

    public List<FileInfoBase> getAll() {
        return fileMapper.selectList(null);
    }

    public void insertOrUpdateFileInfo(File file, int updateUserid, String description) {
        String fileMd5 = BaseTools.getFileMd5(file);
        if (fileMd5 == null) {
            return;
        }
        String relativePath = BaseTools.getFileRelativePath(file);
        if (description == null) {
            description = "No description.";
        }
        String finalDescription = description;
        FileInfoBase newFileInfo = new FileInfoBase() {{
            setFilename(relativePath);
            setHash(fileMd5);
            setUpdateTime(System.currentTimeMillis() / 1000);
            setUpdateUserid(updateUserid);
            setDescription(finalDescription);
        }};

        QueryWrapper<FileInfoBase> wrapper = new QueryWrapper<>();
        wrapper.eq("filename", relativePath);
        FileInfoBase i = fileMapper.selectOne(wrapper);
        if (i == null) {
            logger.info("添加文件: " + relativePath);
            fileMapper.insert(newFileInfo);
            return;
        }

        if (i.getFilename().equals(relativePath)) {
            if (!i.getHash().equals(fileMd5)) {
                logger.info("更新文件: " + relativePath);
                fileMapper.update(newFileInfo, wrapper);
            }
        }
    }

    public void syncDeleteFileInDb(List<File> allFiles) {
        List<String> localFileNames = new ArrayList<>();
        for (File i : allFiles) {
            String relativePath = BaseTools.getFileRelativePath(i);
            localFileNames.add(relativePath);
        }
        List<FileInfoBase> allFilesInDb = getAll();
        for (FileInfoBase i : allFilesInDb) {
            if (!localFileNames.contains(i.getFilename())) {
                QueryWrapper<FileInfoBase> wrapper = new QueryWrapper<>();
                wrapper.eq("filename", i.getFilename());
                fileMapper.delete(wrapper);
                logger.info("删除数据库冗余文件: " + i.getFilename());
            }
        }
    }

    public String checkFileNameAndHash(String fileName, String hash) {
        QueryWrapper<FileInfoBase> wrapper = new QueryWrapper<>();
        wrapper.eq("filename", fileName)
                .eq("hash", hash);
        FileInfoBase result = fileMapper.selectOne(wrapper);
        if (result == null) {
            return null;
        }
        return result.getFilename();
    }

    public boolean deleteFileFromDb(String filename) {
        QueryWrapper<FileInfoBase> wrapper = new QueryWrapper<>();
        wrapper.eq("filename", filename);
        return fileMapper.delete(wrapper) > 0;
    }

    // 反向查找, 暂时没用
    public FileInfoBase checkUserFile(List<FileInfoBase> fileInfoBaseList, String userFilename, String UserFileHash) {
        for (FileInfoBase i : fileInfoBaseList) {
            if (i.getFilename().contains(userFilename)) {
                if (i.getHash().contains(UserFileHash)) {
                    return null;  // 文件相同
                }
                return i;  // 文件需要更新
            }
        }
        return null;  // 服务器没有该文件
    }

    public FileInfoBase checkUserFile(String userFilename, String UserFileHash) {
        List<FileInfoBase> fileInfoBaseList = getAll();
        return checkUserFile(fileInfoBaseList, userFilename, UserFileHash);
    }

}
