echo "1. 获取当前分支最新代码"
git pull

echo "2. 安装node依赖"
docker build . -f dockerfiles/dockerfile-env -t node-env:latest

echo "3. 编译文件"
NEW_DIST_PATH=$(pwd)/dist_latest
mkdir -p ${NEW_DIST_PATH}
docker run --rm -it -v ${NEW_DIST_PATH}:/app/dist node-env:latest npm run build

echo "4. 备份数据, 更新dist目录"
DIST_PATH=$(pwd)/dist
BACKUP_PATH="backup/dist.$(date +%Y%m%d%H%M).bak"
if [ -d ${DIST_PATH} ];then
    mv ${DIST_PATH} ${BACKUP_PATH}
fi
mv ${NEW_DIST_PATH} ${DIST_PATH}

echo "5. 重启nginx"
sudo nginx -s reload