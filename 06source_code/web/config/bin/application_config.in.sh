#!/bin/sh

# check in case a user was using this mechanism
if [ "x$PIGGYCONFIG_CLASSPATH" != "x" ]; then
    cat >&2 << EOF
Error: Don't modify the classpath with PIGGYCONFIG_CLASSPATH.
Add plugins and their dependencies into the plugins/ folder instead.
EOF
    exit 1
fi
PIGGYCONFIG_CLASSPATH=$PIGGYCONFIG_HOME/lib/config.jar:$PIGGYCONFIG_HOME/etc
if [ "x$PIGGYCONFIG_MIN_MEM" = "x" ]; then
    PIGGYCONFIG_MIN_MEM=256m
fi
if [ "x$PIGGYCONFIG_HEAP_SIZE" != "x" ]; then
    PIGGYCONFIG_MIN_MEM=$PIGGYCONFIG_HEAP_SIZE
    PIGGYCONFIG_MAX_MEM=$PIGGYCONFIG_HEAP_SIZE
fi
# min and max heap sizes should be set to the same value to avoid
# stop-the-world GC pauses during resize, and so that we can lock the
# heap in memory on startup to prevent any of it from being swapped
# out.
JAVA_OPTS="$JAVA_OPTS -Xms${PIGGYCONFIG_MIN_MEM}"
if [ "x$PIGGYCONFIG_MAX_MEM" != "x" ]; then
    JAVA_OPTS="$JAVA_OPTS -Xmx${PIGGYCONFIG_MAX_MEM}"
fi
# new generation
if [ "x$PIGGYCONFIG_HEAP_NEWSIZE" != "x" ]; then
    JAVA_OPTS="$JAVA_OPTS -Xmn${PIGGYCONFIG_HEAP_NEWSIZE}"
fi
# max direct memory
if [ "x$PIGGYCONFIG_DIRECT_SIZE" != "x" ]; then
    JAVA_OPTS="$JAVA_OPTS -XX:MaxDirectMemorySize=${PIGGYCONFIG_DIRECT_SIZE}"
fi
# set to headless, just in case
JAVA_OPTS="$JAVA_OPTS -Djava.awt.headless=true"
# Force the JVM to use IPv4 stack
if [ "x$PIGGYCONFIG_USE_IPV4" != "x" ]; then
  JAVA_OPTS="$JAVA_OPTS -Djava.net.preferIPv4Stack=true"
fi
JAVA_OPTS="$JAVA_OPTS -XX:+UseParNewGC"
JAVA_OPTS="$JAVA_OPTS -XX:+UseConcMarkSweepGC"
JAVA_OPTS="$JAVA_OPTS -XX:CMSInitiatingOccupancyFraction=75"
JAVA_OPTS="$JAVA_OPTS -XX:+UseCMSInitiatingOccupancyOnly"
# GC logging options
if [ "x$PIGGYCONFIG_USE_GC_LOGGING" != "x" ]; then
  JAVA_OPTS="$JAVA_OPTS -XX:+PrintGCDetails"
  JAVA_OPTS="$JAVA_OPTS -XX:+PrintGCTimeStamps"
  JAVA_OPTS="$JAVA_OPTS -XX:+PrintGCDateStamps"
  JAVA_OPTS="$JAVA_OPTS -XX:+PrintClassHistogram"
  JAVA_OPTS="$JAVA_OPTS -XX:+PrintTenuringDistribution"
  JAVA_OPTS="$JAVA_OPTS -XX:+PrintGCApplicationStoppedTime"
  GC_LOG_DIR="$PIGGYCONFIG_HOME/logs";
  JAVA_OPTS="$JAVA_OPTS -Xloggc:$GC_LOG_DIR/gc.log"
  # Ensure that the directory for the log file exists: the JVM will not create it.
  if [[ ! -d "$GC_LOG_DIR" ||  ! -x "$GC_LOG_DIR" ]]; then
    cat >&2 << EOF
Error: GC log directory '$GC_LOG_DIR' does not exist or is not accessible.
EOF
    exit 1
  fi
fi
# Disables explicit GC
JAVA_OPTS="$JAVA_OPTS -XX:+DisableExplicitGC"
# Ensure UTF-8 encoding by default (e.g. filenames)
JAVA_OPTS="$JAVA_OPTS -Dfile.encoding=UTF-8"
# Use our provided JNA always versus the system one
JAVA_OPTS="$JAVA_OPTS -Djna.nosys=true"
# log4j options
JAVA_OPTS="$JAVA_OPTS -Dlog4j.shutdownHookEnabled=false -Dlog4j2.disable.jmx=true -Dlog4j.skipJansi=true"