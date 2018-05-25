create_namespace 'uni'

create 'uni:user', {NAME => 'info', VERSIONS => 1}, {NAME => 'statusid', DFS_REPLICATION => 1}
 

create 'uni:content', {NAME => 'info', VERSIONS => 1}, {NAME => 'keywords', DFS_REPLICATION => 1}, {NAME => 'entity', DFS_REPLICATION => 1}


create 'uni:comment', {NAME => 'info', VERSIONS => 1}, {NAME => 'text', DFS_REPLICATION => 1}, {NAME => 'entity', DFS_REPLICATION => 1}


create 'uni:relation', {NAME => 'focus', VERSIONS => 1}, {NAME => 'follwers', DFS_REPLICATION => 1}
