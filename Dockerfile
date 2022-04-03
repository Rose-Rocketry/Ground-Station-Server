# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT=3.9-bullseye
FROM python:${VARIANT}

ENV PYTHONUNBUFFERED 1
WORKDIR /Rocketry

# [Optional] If your requirements rarely change, uncomment this section to add them to the image.
 COPY requirements.txt /tmp/pip-tmp/
 RUN pip -v install --index-url https://www.piwheels.org/simple cryptography
 RUN pip  --disable-pip-version-check --no-cache-dir install --index-url https://www.piwheels.org/simple --extra-index-url https://pypi.org/simple/ -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
COPY ./GroundStation/ /Rocketry

CMD ["daphne" "GroundStation.asgi:application"]
