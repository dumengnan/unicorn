#!/bin/sh

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  current_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$current_dir/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done

# 获取当前工作目录
current_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
MYAPPLICATION_HOME="$current_dir"/..

if [ "x$MYAPPLICATION_INCLUDE" = "x" ]; then
    for include in $MYAPPLICATION_HOME/bin/myapp.in.sh; do
        if [ -r $include ]; then
            . $include
            break
        fi
    done
elif [ -r $MYAPPLICATION_INCLUDE ]; then
    . $MYAPPLICATION_INCLUDE
fi

if [ -x "$JAVA_HOME/bin/java" ]; then
    JAVA="$JAVA_HOME/bin/java"
else
    JAVA=`which java`
fi

if [ ! -x "$JAVA" ]; then
    echo "Could not find any executable java binary. Please install java in your PATH or set JAVA_HOME"
    exit 1
fi

if [ -z $MYAPPLICATION_CLASSPATH ]; then
    echo "You must set the  CLASSPATH vars" >&2
    exit 1
fi

# Special-case path variables.
case "`uname`" in
    CYGWIN*) 
        MYAPPLICATION_CLASSPATH=`cygpath -p -w "$MYAPPLICATION_CLASSPATH"`
        MYAPPLICATION_CONF=`cygpath -p -w "$MYAPPLICATION_CONF"`
    ;;
esac

# 默认后台启动
# The option will tell MYAPPLICATIONDaemon not
# to close stdout/stderr, but it's up to us not to background.
if [ "x$daemonized" != "x" ]; then
    exec $JAVA $JAVA_OPTS  -cp $MYAPPLICATION_CLASSPATH -DrootDir=$MYAPPLICATION_HOME \
            org.springframework.boot.loader.JarLauncher  "$@"
# Startup piggy config , background it
else
    exec $JAVA $JAVA_OPTS  -cp $MYAPPLICATION_CLASSPATH -DrootDir=$MYAPPLICATION_HOME \
                org.springframework.boot.loader.JarLauncher "$@" <&- &
fi


exit $?
