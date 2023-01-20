package com.chinosk.uma.upd.server.www;

import com.chinosk.uma.upd.server.Annotations.UmaUserPermission;
import com.chinosk.uma.upd.server.dbaccessobj.FileInfoDAO;
import com.chinosk.uma.upd.server.dbaccessobj.UmaUsersDAO;
import com.chinosk.uma.upd.server.models.FileInfoBase;
import com.chinosk.uma.upd.server.models.FileInfoWithUserName;
import com.chinosk.uma.upd.server.processor.FileController;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static com.chinosk.uma.upd.server.dbaccessobj.UmaUsersDAO.*;
import static com.chinosk.uma.upd.server.processor.FileController.transFileBasePath;

@Controller
public class MainController {
    @ResponseBody
    @RequestMapping(value = "/hello", method = {RequestMethod.POST})
    public ResponseEntity<HashMap<String, Object>> hello(@RequestHeader Map<String, String> headers,
                                                         @RequestParam Map<String, String> param,
                                                         @RequestBody Map<String, String> body) {
        String token = headers.get("token");
        String p1 = param.get("p1");
        String b1 = body.get("b1");

        HashMap<String, Object> ret = new HashMap<>();
        ret.put("gettoken", token);
        ret.put("p1", p1);
        ret.put("b1", b1);
        ret.put("haha", 100);

        HttpHeaders retheaders = new HttpHeaders();
        retheaders.add("mystat", "online");
        return ResponseEntity.status(418)
                .headers(retheaders)
                .body(ret);
    }

    public static ResponseEntity<HashMap<String, Object>> returnGenerator(
            int status, boolean isSuccess, String msg, Object data) {
        HashMap<String, Object> ret = new HashMap<>();
        ret.put("success", isSuccess);
        ret.put("message", msg);
        ret.put("data", data);
        return ResponseEntity.status(status)
                .body(ret);
    }

    @UmaUserPermission(minPermission = READ_LIST_ONLY)
    @ResponseBody
    @RequestMapping(value = "/api/get_all_files", method = {RequestMethod.GET})
    public ResponseEntity<HashMap<String, Object>> getAllFiles(@RequestHeader Map<String, String> headers,
                                                         @RequestParam Map<String, String> param) {

        FileInfoDAO fileInfoDAO = FileInfoDAO.getInstance();
        UmaUsersDAO umaUsersDAO = UmaUsersDAO.getInstance();
        List<FileInfoBase> ret = fileInfoDAO.getAll();
        List<FileInfoWithUserName> retEx = new ArrayList<>();
        HashMap<Integer, String> userNames = new HashMap<>();
        for (FileInfoBase i : ret) {
            String userName;
            if (userNames.containsKey(i.getUpdateUserid())) {
                userName = userNames.get(i.getUpdateUserid());
            }
            else {
                userName = umaUsersDAO.getUserNameFromUID(i.getUpdateUserid());
                userNames.put(i.getUpdateUserid(), userName);
            }
            FileInfoWithUserName fileInfoWithUserName = new FileInfoWithUserName(i, userName);
            retEx.add(fileInfoWithUserName);
        }
        return returnGenerator(200, true, "success", retEx);
    }

    @UmaUserPermission(minPermission = READ_WRITE)
    @ResponseBody
    @RequestMapping(value = "/api/post_file", method = {RequestMethod.POST})
    public ResponseEntity<HashMap<String, Object>> postFile(@RequestHeader Map<String, String> headers,
                                                            @RequestParam("file") MultipartFile file,
                                                            @RequestParam("filename") String fileName,
                                                            @RequestParam("description") String description) {
        if (file.isEmpty() || fileName == null) {
            return returnGenerator(400, false, "Bad Request", null);
        }

        try {
            String basePath = transFileBasePath.replace("\\", "/");
            if (!fileName.startsWith("/")) {
                fileName = "/" + fileName;
            }
            String saveName = basePath + fileName;
            File saveFile = new File(saveName);

            Path folderName = Path.of(saveFile.getParent());
            if (!Files.isDirectory(folderName)) {
                Files.createDirectories(folderName);
            }

            BufferedOutputStream out = new BufferedOutputStream(
                    new FileOutputStream(saveFile));
            out.write(file.getBytes());
            out.flush();
            out.close();
            int userUID = UmaUsersDAO.getInstance().getUserInfoByToken(headers.get("token")).getUid();
            FileInfoDAO.getInstance().insertOrUpdateFileInfo(saveFile, userUID, description);
        } catch (Exception e) {
            return returnGenerator(500, false, "Exception Occurred: " + e, null);
        }
        return returnGenerator(200, true, "success", null);
    }

    @UmaUserPermission(minPermission = ADMIN)
    @ResponseBody
    @RequestMapping(value = "/api/add_user", method = {RequestMethod.GET})
    public ResponseEntity<HashMap<String, Object>> addUser(@RequestParam Map<String, String> param) {
        int permission;
        String userName;
        try {
            userName = param.get("name");
            permission = Integer.parseInt(param.get("permission"));
        }
        catch (Exception ex) {
            return returnGenerator(400, false, "invalid input", null);
        }
        Map<String, Object> data = UmaUsersDAO.getInstance().addUser(userName, permission);
        return returnGenerator(200, true, "success", data);
    }

    @UmaUserPermission(minPermission = OWNER)
    @ResponseBody
    @RequestMapping(value = "/api/del_user", method = {RequestMethod.GET})
    public ResponseEntity<HashMap<String, Object>> delUser(@RequestParam Map<String, String> param) {
        String userToken = param.get("deleteToken");
        String userUID = param.get("deleteUID");
        UmaUsersDAO umaUsersDAO = UmaUsersDAO.getInstance();
        boolean success = false;
        if (userToken != null) {
            success = umaUsersDAO.deleteUser(userToken);
        }
        else {
            if (userUID != null) {
                try {
                    int uid = Integer.parseInt(userUID);
                    success = umaUsersDAO.deleteUser(uid);
                }
                catch (Exception ignored){}
            }
        }
        return returnGenerator(200, success, "done.", null);
    }

    @UmaUserPermission(minPermission = READ_WRITE)
    @ResponseBody
    @RequestMapping(value = "/api/delete_file", method = {RequestMethod.DELETE})
    public ResponseEntity<HashMap<String, Object>> delFile(@RequestParam Map<String, String> param) {
        String filename = param.get("filename");
        if (filename == null) {
            return returnGenerator(400, false, "Missing required param.", null);
        }

        FileInfoDAO fileInfoDAO = FileInfoDAO.getInstance();
        if (fileInfoDAO.deleteFileFromDb(filename)) {
            if (FileController.deleteLocalFile(filename)) {
                return returnGenerator(200, true, "success", null);
            }
        }
        return returnGenerator(404, false, "failed", null);
    }

    @ResponseBody
    @RequestMapping(value = "/api/get_userinfo", method = {RequestMethod.GET})
    public ResponseEntity<HashMap<String, Object>> getUserinfo(@RequestHeader Map<String, String> param) {
        String token = param.get("token");
        UmaUsersDAO umaUsersDAO = UmaUsersDAO.getInstance();
        return returnGenerator(200, true, "userinfo", umaUsersDAO.getUserInfoByToken(token));
    }

    @ResponseBody
    @RequestMapping(value = "/api/update_token", method = {RequestMethod.GET})
    public ResponseEntity<HashMap<String, Object>> updateToken(@RequestHeader Map<String, String> headers,
                                                               @RequestParam Map<String, String> param) {
        String token = headers.get("token");
        String newToken = param.get("new_token");
        UmaUsersDAO umaUsersDAO = UmaUsersDAO.getInstance();
        if ((newToken == null) || newToken.equals("")) {
            newToken = umaUsersDAO.changeToken(token);
        }
        else {
            if (!umaUsersDAO.changeToken(token, newToken)) {
                newToken = null;
            }
        }
        return returnGenerator(200, newToken != null, "userinfo", newToken);
    }

    @ResponseBody
    @RequestMapping(value = "/file/get", method = {RequestMethod.GET})
    public ResponseEntity<HashMap<String, Object>> getFile(HttpServletResponse response,
                                                           @RequestParam Map<String, String> param) {
        String filename = param.get("filename");
        String hash = param.get("hash");
        filename = FileInfoDAO.getInstance().checkFileNameAndHash(filename, hash);
        if (filename == null) {
            return returnGenerator(403, false, "Permission Denied.", null);
        }

        String basePath = transFileBasePath.replace("\\", "/");
        String fileFullPath = basePath + "/" + filename;
        File file = new File(fileFullPath);
        if (!file.exists()) {
            return returnGenerator(404, false, "File not found.", null);
        }

        response.reset();
        response.setContentType("application/octet-stream");
        // response.setCharacterEncoding("utf-8");
        response.setContentLength((int) file.length());
        // response.setHeader("Content-Disposition", "attachment;filename=" + file.getName() );
        try(BufferedInputStream bis = new BufferedInputStream(new FileInputStream(file))) {
            byte[] buff = new byte[1024];
            OutputStream os  = response.getOutputStream();
            int i = 0;
            while ((i = bis.read(buff)) != -1) {
                os.write(buff, 0, i);
                os.flush();
            }
            return null;
        }
        catch (IOException e) {
            return returnGenerator(500, false, "Exception Occurred", null);
        }
    }

    @ResponseBody
    @RequestMapping(value = "/file/get_list", method = {RequestMethod.POST})
    public ResponseEntity<HashMap<String, Object>> requestFileList(@RequestBody Map<String, String> param) {
        FileInfoDAO fileInfoDAO = FileInfoDAO.getInstance();
        List<FileInfoBase> fileInfoBaseList = fileInfoDAO.getAll();
        Map<String, Map<String, String>> ret = new HashMap<>();
        HashMap<Integer, String> userNames = new HashMap<>();

        for (FileInfoBase i : fileInfoBaseList) {
            String userName;
            if (userNames.containsKey(i.getUpdateUserid())) {
                userName = userNames.get(i.getUpdateUserid());
            }
            else {
                userName = umaUsersDAO.getUserNameFromUID(i.getUpdateUserid());
                userNames.put(i.getUpdateUserid(), userName);
            }

            if (param.containsKey(i.getFilename())) {
                String userFileHash = param.get(i.getFilename());
                if (!i.getHash().equals(userFileHash)) {
                    Map<String, String> putData = new HashMap<>(){{
                       put("hash", i.getHash());
                       put("user", userName);
                       put("desc", i.getDescription());
                    }};
                    ret.put(i.getFilename(), putData);
                }
            }
            else {
                Map<String, String> putData = new HashMap<>(){{
                    put("hash", i.getHash());
                    put("user", userName);
                    put("desc", i.getDescription());
                }};
                ret.put(i.getFilename(), putData);
            }
        }
        return returnGenerator(200, true, "success", ret);
    }

}
