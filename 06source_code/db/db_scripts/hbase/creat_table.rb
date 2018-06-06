create_namespace 'uni'

create 'uni:user', {NAME => 'info', VERSIONS => 1}, {NAME => 'statusid', VERSIONS => 1}
 

create 'uni:content', {NAME => 'info', VERSIONS => 1}, {NAME => 'keywords', VERSIONS => 1}, {NAME => 'entity', VERSIONS => 1}


create 'uni:comment', {NAME => 'info', VERSIONS => 1}, {NAME => 'text', VERSIONS => 1}, {NAME => 'entity', VERSIONS => 1}


create 'uni:relation', {NAME => 'focus', VERSIONS => 1}, {NAME => 'follwers', VERSIONS => 1}
