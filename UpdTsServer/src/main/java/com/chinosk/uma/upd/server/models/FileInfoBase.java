package com.chinosk.uma.upd.server.models;

import com.baomidou.mybatisplus.annotation.OrderBy;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("files")
public class FileInfoBase {
    @OrderBy(asc=true)
    private String filename;
    private String hash;
    private long updateTime;
    private int updateUserid;
    private String description;

    public void setFilename(String filename) {
        this.filename = filename;
    }
    public String getFilename() {
        return filename;
    }

    public void setHash(String hash) {
        this.hash = hash;
    }
    public String getHash() {
        return hash;
    }

    public void setUpdateTime(long updateTime) {
        this.updateTime = updateTime;
    }
    public long getUpdateTime() {
        return updateTime;
    }

    public void setUpdateUserid(int updateUserId) {
        this.updateUserid = updateUserId;
    }
    public int getUpdateUserid() {
        return updateUserid;
    }

    public void setDescription(String description) {
        this.description = description;
    }
    public String getDescription() {
        return description;
    }

}