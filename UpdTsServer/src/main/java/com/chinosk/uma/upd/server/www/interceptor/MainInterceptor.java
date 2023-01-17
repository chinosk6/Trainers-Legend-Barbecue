package com.chinosk.uma.upd.server.www.interceptor;

import com.alibaba.fastjson.JSONObject;
import com.chinosk.uma.upd.server.Annotations.UmaUserPermission;
import com.chinosk.uma.upd.server.dbaccessobj.UmaUsersDAO;
import com.chinosk.uma.upd.server.models.UmaUsers;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;

import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Objects;



public class MainInterceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        HandlerMethod handlerMethod = (HandlerMethod) handler;
        Method method = handlerMethod.getMethod();
        UmaUserPermission userAuthenticate = method.getAnnotation(UmaUserPermission.class);

        if (Objects.nonNull(userAuthenticate)) {
            String token = request.getHeader("token");
            UmaUsersDAO umaUsersDAO = UmaUsersDAO.getInstance();
            UmaUsers userInfo = umaUsersDAO.getUserInfoByToken(token);
            HashMap<Object, Object> ret = new HashMap<>();
            if (userInfo == null) {
                response.setStatus(401);
                response.setCharacterEncoding("UTF-8");
                response.setContentType("application/json");
                ret.put("success", false);
                ret.put("message", "Unauthorized");
                response.getWriter().println(JSONObject.toJSONString(ret));
                return false;
            }

            if (userInfo.getPermission() < userAuthenticate.minPermission()) {
                response.setStatus(403);
                response.setCharacterEncoding("UTF-8");
                response.setContentType("application/json");
                ret.put("success", false);
                ret.put("message", "Permission Denied");
                response.getWriter().println(JSONObject.toJSONString(ret));
                return false;
            }
        }
        return true;
    }

}
