SHELL=/bin/sh
PYTHON=python3
BUILD_DIR=/opt/build/
DIST_DIR=/opt/dist/
FINAL_FUNCTION_DIR=${BUILD_DIR}function
DIST_PACKAGE=function.zip

.PHONY = clean init package

.DEFAULT_GOAL = build

clean:
	(\
		rm -rf ${BUILD_DIR}; \
		rm -rf ${DIST_DIR}; \
	)

init:
	(\
		mkdir ${BUILD_DIR}; \
		mkdir ${DIST_DIR}; \
		mkdir ${FINAL_FUNCTION_DIR}; \
		apk update && apk add zip; \
		${PYTHON} -m pip install --upgrade pip; \
		${PYTHON} -m pip install virtualenv; \
	)

package:
	(\
		cp -r ./* ${FINAL_FUNCTION_DIR}; \
		${PYTHON} -m virtualenv ${BUILD_DIR}; \
		source ${BUILD_DIR}/bin/activate; \
		${PYTHON} -m pip install --upgrade pip; \
		${PYTHON} -m pip install -r ./requirements.txt --target=${FINAL_FUNCTION_DIR}/; \
		deactivate; \
		cd ${BUILD_DIR}; \
		zip -r9 ${DIST_DIR}${DIST_PACKAGE} . ; \
	)

build: clean init package
