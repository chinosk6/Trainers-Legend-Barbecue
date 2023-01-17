package com.chinosk.uma.upd.server.dbaccessobj;

import ch.qos.logback.core.joran.sanity.Pair;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.chinosk.uma.upd.server.mapper.UmaUsersMapper;
import com.chinosk.uma.upd.server.models.UmaUsers;
import com.chinosk.uma.upd.server.processor.BaseTools;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

@Component
public class UmaUsersDAO {
    private final UmaUsersMapper usersMapper;
    public static UmaUsersDAO umaUsersDAO;

    public static final int READ_LIST_ONLY = 1;  // 只读列表
    public static final int READ_ALL_ONLY = 2;  // 只读, 可读内容
    public static final int READ_WRITE = 3;  // 可读可写
    public static final int ADMIN = 4;  // 可增用户, 不可删用户
    public static final int OWNER = 5;  // 可增删用户

    @Autowired
    public UmaUsersDAO(UmaUsersMapper usersMapper) {
        MapperSaver.setUmaUsersMapper(usersMapper);
        this.usersMapper = usersMapper;
        umaUsersDAO = this;
    }

    public UmaUsersDAO() {
        this.usersMapper = MapperSaver.getUmaUsersMapper();
        umaUsersDAO = this;
    }

    public static UmaUsersDAO getInstance() {
        if (umaUsersDAO == null) {
            new UmaUsersDAO();
        }
        return umaUsersDAO;
    }

    public List<UmaUsers> getAll() {
        return usersMapper.selectList(null);
    }

    public UmaUsers getUserInfoByToken(String token) {
        QueryWrapper<UmaUsers> wrapper = new QueryWrapper<>();
        wrapper.eq("token", token);
        return usersMapper.selectOne(wrapper);
    }

    public String getUserNameFromUID(Integer userid) {
        QueryWrapper<UmaUsers> wrapper = new QueryWrapper<>();
        wrapper.eq("uid", userid);
        UmaUsers umaUser = usersMapper.selectOne(wrapper);
        if (umaUser == null) {
            return userid.toString();
        }
        return umaUser.getName();
    }

    public boolean deleteUser(int userid) {
        QueryWrapper<UmaUsers> wrapper = new QueryWrapper<>();
        wrapper.eq("uid", userid);
        return usersMapper.delete(wrapper) > 0;
    }

    public boolean deleteUser(String token) {
        QueryWrapper<UmaUsers> wrapper = new QueryWrapper<>();
        wrapper.eq("token", token);
        return usersMapper.delete(wrapper) > 0;
    }

    public Map<String, Object> addUser(String name, int permission) {
        String token = BaseTools.getRandomString(18);
        QueryWrapper<UmaUsers> wrapper = new QueryWrapper<>();
        wrapper.eq("token", token);
        if (usersMapper.selectCount(wrapper) > 0) {
            return addUser(name, permission);
        }
        UmaUsers umaUser = new UmaUsers(){{
            setUid(null);
            setName(name);
            setPermission(permission);
            setToken(token);
        }};
        usersMapper.insert(umaUser);
        return new HashMap<>() {{
            put("token", token);
            put("uid", umaUser.getUid());
        }};
    }

}
