package com.sz.auth.domain;

import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import javax.persistence.ElementCollection;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import javax.validation.constraints.NotNull;

@Entity
@Table(name = "oauth_client_details")
public class CustomClientDetails {

    @Id
    @NotNull
    private String clientId;
    private String clientSecret;
    private String resourceIds;
    private boolean secretRequired;
    private String scope;
    private String authorizedGrantTypes;
    private Set<String> registeredRedirectUri;
    private Collection<String> authorities;
    private Integer accessTokenValidity;
    private  Integer refreshTokenValidity;
    private boolean autoApprove;
    private String additionalInformation;

}
