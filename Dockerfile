FROM meteogroup/hpc_tools 

COPY requirements.txt .
COPY docker-entrypoint.sh /usr/local/bin/
RUN source /etc/profile.d/modules.sh && \
    module load ecflow/gcc/current && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt 

##### Install our application / library
WORKDIR /src
COPY . .

ENTRYPOINT ["docker-entrypoint.sh"]
