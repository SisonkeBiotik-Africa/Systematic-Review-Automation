#!/usr/bin/env bash

## image name ##
PATH_IMAGE_NAME=${PWD}/.container_image_name
if [ -f ${PATH_IMAGE_NAME} ]
then
  CONTAINER_IMAGE_NAME=$(cat ${PATH_IMAGE_NAME})
else 
  CONTAINER_IMAGE_NAME=${PWD##*/} 
  # use lowercase dev directory name as image name 
  echo  sisonkebiotik/${CONTAINER_IMAGE_NAME,,} >> ${PATH_IMAGE_NAME}
fi

docker build -t sisonkebiotik/${CONTAINER_IMAGE_NAME,,} \
--build-arg USER=${USER} --build-arg USERID=$(id -u) \
.