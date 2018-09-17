package com.sz.auth.repository.mapper;

import com.sz.auth.domain.User;

/**
 * Created by Administrator on 2017/6/3.
 */
public interface UserMapper {
     User findUser(String userName);
     void createUser(User user);
}
