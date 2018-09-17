package com.sz.auth.service.security;

import com.sz.auth.domain.User;
import com.sz.auth.repository.mapper.UserMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

/**
 * Created by Administrator on 2017/7/8.
 */
@Service
public class MysqlUserDetailsService implements UserDetailsService {

    @Autowired
    private UserMapper repository;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {

        User user = repository.findUser(username);

        if (user == null) {
            throw new UsernameNotFoundException(username);
        }

        return user;
    }

}
