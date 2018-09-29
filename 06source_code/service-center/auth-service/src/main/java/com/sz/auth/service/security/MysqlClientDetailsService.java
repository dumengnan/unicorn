package com.sz.auth.service.security;

import com.sz.auth.domain.CustomClientDetails;
import com.sz.auth.repository.CustomClientDetailsRepository;
import java.util.Arrays;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.oauth2.provider.ClientDetails;
import org.springframework.security.oauth2.provider.ClientDetailsService;
import org.springframework.security.oauth2.provider.ClientRegistrationException;
import org.springframework.security.oauth2.provider.client.BaseClientDetails;
import org.springframework.stereotype.Service;
import org.springframework.transation.annotation.Transactional;

@Service
@Transactional
public class MysqlClientDetailsService implements ClientDetailsService {

    @Autowired
    private CustomClientDetailsRepository customClientDetailsRepository;

    @Override
    public ClientDetails loadClientByClientId(String clientId) throws ClientRegistrationException {

        CustomClientDetails client = customClientDetailsRepository.findByClientId(clientId);

        String resourceIds = client.getResourceIds();
        String scopes = client.getScope();
        String grantTypes = client.getAuthorizedGrantTypes();
        String authorities = client.getAuthorities();

        BaseClientDetails base = new BaseClientDetails(client.getClientId(), resourceIds, scopes, grantTypes, authorities);
        base.setClientSecret(client.getClientSecret());
        base.setAccessTokenValiditySeconds(client.getAccessTokenValidity());
        base.setRefreshTokenValiditySeconds(client.getRefreshTokenValidity());
        base.setAutoApproveScopes(Arrays.asList(client.getScope().split(",")));
        return base;
    }
}
