
[docker@kfdct070 ~]$ for container in $(docker ps -a --format '{{ .ID }}'); do policy=$(docker inspect $container --format '{{ .HostConfig.RestartPolicy.Name }}'); echo $container $policy; done | grep always

for container in $(docker ps -a --format '{{ .ID }}'); do policy=$(docker inspect $container --format '{{ .HostConfig.RestartPolicy.Name }}'); echo $container $policy; done | grep always

docker logs -f --tail 100

for container in $(docker ps -a --format '{{ .Names }}'); do policy=$(docker logs --tail 100 $container ); echo "\n\\n\n\n\n\n",$container , $policy; $container ;sleep 3; done 

  846  docker run -d --name=hlog-metricbeat --mount type=bind,source=/proc,target=/hostfs/proc,readonly --mount type=bind,source=/sys/fs/cgroup,target=/hostfs/sys/fs/cgroup,readonly --mount type=bind,source=/,target=/hostfs,readonly --log-opt max-size=10m --log-opt max-file=3 --net=host metricbeat:7.6.2 -e -system.hostfs=/hostfs
  848  docker run -d --name=hlog-metricbeat --mount type=bind,source=/proc,target=/hostfs/proc,readonly --mount type=bind,source=/sys/fs/cgroup,target=/hostfs/sys/fs/cgroup,readonly --mount type=bind,source=/,target=/hostfs,readonly --log-opt max-size=10m --log-opt max-file=3 --net=host metricbeat:latest -e -system.hostfs=/hostfs
  882  docker run -d --name=hlog-metricbeat --mount type=bind,source=/proc,target=/hostfs/proc,readonly --mount type=bind,source=/sys/fs/cgroup,target=/hostfs/sys/fs/cgroup,readonly --mount type=bind,source=/,target=/hostfs,readonly --log-opt max-size=10m --log-opt max-file=3 --net=host metricbeat:latest -e -system.hostfs=/hostfs
  977  vi build-and-run.sh
 1011      docker run -d --name=hlog-filebeat --volume="/var/lib/docker/containers:/var/lib/docker/containers" --volume="/var/run/docker.sock:/var/run/docker.sock:ro" --log-opt max-size=10m --log-opt max-file=3 --net=host filebeat:7.6.2 -e -system.hostfs=/hostfs
 1012  docker run -d --name=hlog-filebeat --volume="/var/lib/docker/containers:/var/lib/docker/containers" --volume="/var/run/docker.sock:/var/run/docker.sock:ro" --log-opt max-size=10m --log-opt max-file=3 --net=host filebeat:7.6.2 -e -system.hostfs=/hostfs
 
 
