BUILD_TOOL_DIR='/group/it/tools/frontend/'
PROJECT_ROOT='/group/it/productions/frontend'

ls $PROJECT_ROOT
read -p "1. 输入项目名称: " SERVICE_NAME
PROJECT_DIR=$PROJECT_ROOT/$SERVICE_NAME

_BUILD_CMD="npm run test"
case "$SERVICE_NAME" in
    "demo")
        _BUILD_CMD="npm test";;
esac

read -p "2. 编译命令: $_BUILD_CMD ?" BUILD_CMD
if [ "${BUILD_CMD}" == "" ];then
    BUILD_CMD=$_BUILD_CMD;
fi
echo "编译命令:" $BUILD_CMD

echo "2. 获取当前分支最新代码"
echo $PROJECT_DIR
cd $PROJECT_DIR && git pull
if [ $? != 0 ];then
    exit 1;
fi

echo "3. 编译镜像，安装依赖包"
SERVICE_IMAGE=${SERVICE_NAME}-frontend-env:latest
docker images -q ${SERVICE_IMAGE} | grep -q .
if [ $? != 0 ];then
    docker pull node:22.3.0 && docker tag node:22.3.0 ${SERVICE_IMAGE}
fi
cp ${BUILD_TOOL_DIR}/.dockerignore ${PROJECT_DIR} # 覆盖.dockerignore文件
cat ${PROJECT_DIR}/.gitignore >> ${PROJECT_DIR}/.dockerignore
docker build ${PROJECT_DIR} -f ${BUILD_TOOL_DIR}/dockerfile --build-arg IMAGE_NAME=${SERVICE_IMAGE} -t ${SERVICE_IMAGE}
echo $BUILD_CMD

echo "4. 编译文件"
NEW_DIST_PATH=${PROJECT_DIR}/dist_latest
mkdir -p ${NEW_DIST_PATH}
# --memory 避免爆内存
docker run --rm -it --memory="2g" --cpus="2" -v ${NEW_DIST_PATH}:/app/dist ${SERVICE_IMAGE} $BUILD_CMD

echo "5. 备份数据, 更新dist目录"
OLD_DIST_PATH=${PROJECT_DIR}/dist
BACKUP_DIR="/group/it/productions/backup/frontend/${SERVICE_NAME}/$(date +%Y%m%d)"
BACKUP_PATH="${BACKUP_DIR}/dist.$(date +%Y%m%d%H%M).bak"
mkdir -p ${BACKUP_DIR}
if [ -d ${OLD_DIST_PATH} ];then
    mv ${OLD_DIST_PATH} ${BACKUP_PATH}
fi
mv ${NEW_DIST_PATH} ${OLD_DIST_PATH}

echo "6. 重启nginx"
sudo nginx -s reload