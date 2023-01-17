package com.chinosk.uma.upd.server.models;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.OrderBy;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("users")
public class UmaUsers {
  @TableId(type = IdType.AUTO) @OrderBy(asc=true)
  private Integer uid;
  private String name;
  private String token;
  private Integer permission;


  public Integer getUid() {
    return uid;
  }

  public void setUid(Integer uid) {
    this.uid = uid;
  }


  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }


  public String getToken() {
    return token;
  }

  public void setToken(String token) {
    this.token = token;
  }


  public int getPermission() {
    return permission;
  }

  public void setPermission(int permission) {
    this.permission = permission;
  }

}
