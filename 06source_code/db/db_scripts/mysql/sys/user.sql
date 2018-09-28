CREATE TABLE user(
    id     INTEGER, 
	username varchar(100) NOT NULL PRIMARY KEY,
	password varchar(100), 
	remark varchar(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


create table oauth_client_details (
    client_id VARCHAR(256) PRIMARY KEY,
    resource_ids VARCHAR(256),
    client_secret VARCHAR(256),
    scope VARCHAR(256),
    authorized_grant_types VARCHAR(256),
    web_server_redirect_uri VARCHAR(256),
    authorities VARCHAR(256),
    access_token_validity INTEGER,
    refresh_token_validity INTEGER,
    additional_information VARCHAR(4096),
    autoapprove VARCHAR(256)
);

INSERT INTO oauth_client_details
    (client_id, client_secret, scope, authorized_grant_types,
    web_server_redirect_uri, authorities, access_token_validity,
    refresh_token_validity, additional_information, autoapprove)
VALUES
    ("browser", null, "ui",
    "password,refresh_token", null, null, 36000, 36000, null, true);