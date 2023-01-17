package com.chinosk.uma.upd.server.dbaccessobj;

import com.chinosk.uma.upd.server.mapper.FileInfoMapper;
import com.chinosk.uma.upd.server.mapper.UmaUsersMapper;

public class MapperSaver {
    private static UmaUsersMapper umaUsersMapper;
    private static FileInfoMapper fileInfoMapper;

    public static void setUmaUsersMapper(UmaUsersMapper value) {
        umaUsersMapper = value;
    }

    public static UmaUsersMapper getUmaUsersMapper() {
        return umaUsersMapper;
    }

    public static void setFileInfoMapper(FileInfoMapper value) {
        fileInfoMapper = value;
    }

    public static FileInfoMapper getFileInfoMapper() {
        return fileInfoMapper;
    }

}
