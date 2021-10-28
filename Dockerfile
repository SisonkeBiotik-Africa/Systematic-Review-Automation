FROM python:3.9.7-slim

# pass in build arguments #
ARG USER
ARG USERID

# root installs - some dev tools 
RUN apt update && \
    apt install --yes git sudo curl wget zsh vim nano && \
    apt clean

# add USER 
# create new user and pass in host machine username 
RUN useradd --create-home --uid ${USERID} ${USER}
RUN adduser ${USER} sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
# set working directory to development directory in the user's home directory 
WORKDIR /home/${USER}/dev_dir

# copy project / development directory to container to make files avaiable for install at build time 
COPY . /home/${USER}/dev_dir
# ensure user permissions in dev_dir 
RUN chown -R ${USER} /home/${USER}/dev_dir
RUN chown -R ${USER} /root

# activate the desired user
USER ${USER}

# update pip
RUN python -m pip install --upgrade pip --no-warn-script-location 
# install some useful python tools 
RUN python -m pip install jupyterlab --no-warn-script-location 
# find and pip install local python packages being developed on 
# find and pip install -e . setup.py files
RUN for SETUP in $(find . -mindepth 1 -maxdepth 2 -name setup.py); do \
    python -m pip install --no-warn-script-location --prefix ~/.local --editable $(dirname $SETUP); \
    done && \
    # find and pip install -e . setup.cfg files 
    for CONFIG in $(find . -mindepth 1 -maxdepth 2 -name setup.cfg); do \
    python -m pip install --no-warn-script-location --prefix ~/.local --editable $(dirname $CONFIG)"${EXTRAS_REQUIRE}"; \
    done
# find and pip install -r requirements.txt files 
RUN for REQUIREMENT in $(find . -mindepth 1 -maxdepth 2 -name requirements.txt); do \
    python -m pip install --no-warn-script-location --user --requirement ${REQUIREMENT}; \
    done && \
     # find and pip install -r requirements-dev.txt files 
    for REQUIREMENT_DEV in $(find . -mindepth 1 -maxdepth 2 -name requirements-dev.txt); do \
    python -m pip install --no-warn-script-location --user --requirement ${REQUIREMENT_DEV}; \
    done

# add installed python packages to path 
ENV PATH=/home/${USER}/.local/bin/:$PATH

## Install Oh my Zsh for user 
RUN bash -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
RUN sed -i -- 's/robbyrussell/sonicradish/g' /home/${USER}/.zshrc 

## Run command when container starts 
CMD "zsh"

