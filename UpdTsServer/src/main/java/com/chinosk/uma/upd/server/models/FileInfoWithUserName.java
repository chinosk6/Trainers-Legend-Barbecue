package com.chinosk.uma.upd.server.models;

public class FileInfoWithUserName extends FileInfoBase {
    private String updateUserName;

    public FileInfoWithUserName() {
    }

    public FileInfoWithUserName(FileInfoBase fileInfoBase, String updateUserName) {
        this.setFilename(fileInfoBase.getFilename());
        this.setHash(fileInfoBase.getHash());
        this.setUpdateTime(fileInfoBase.getUpdateTime());
        this.setUpdateUserid(fileInfoBase.getUpdateUserid());
        this.setDescription(fileInfoBase.getDescription());
        this.updateUserName = updateUserName;
    }

    public void setUpdateUserName(String updateUserName) {
        this.updateUserName = updateUserName;
    }

    public String getUpdateUserName() {
        return updateUserName;
    }
}
