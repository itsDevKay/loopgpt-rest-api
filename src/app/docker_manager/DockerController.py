import docker

class DockerController:
    client = docker.from_env()

    def build_image(self, path, tag, dockerfile, buildargs={}, container_limits=[], pull=False, quiet=False):
        try:
            image = self.client.build(
                path=path,
                tag=tag,
                dockerfile=dockerfile,
                buildargs=buildargs,
                container_limits=container_limits,
                pull=pull, quiet=quiet
            )
            # image.save() for getting a tarball of the image
            return image
        except docker.errors.BuildError as e:
            return (None, { 'BuildError': str(e) })
        except docker.errors.APIError as e:
            return (None, { 'APIError': str(e) })
        
    def delete_image(self, image, force=False):
        self.client.remove(image, force)
        return { 'status': 200, 'response': 'Image deleted successfully.'}
    
    def get_image(self, name):
        try:
            image = self.client.get(name)
            return { 'status': 200, 'response': image }
        except docker.errors.ImageNotFound as e:
            return { 'status': 'ImageNotFound', 'response': str(e) }
        except docker.errors.APIError as e:
            return { 'status': 'APIError', 'response': str(e) }
        
    def run_image(self, image, environment={}, command=None, auto_remove=True, detach=True):
        try:
            container = self.client.containers.run(
                image=image,
                environment=environment,
                command=command,
                auto_remove=auto_remove,
                detach=detach
            )
            return { 'status': 200, 'response': container }
        except docker.errors.ContainerError as e:
            return { 'status': 'ContainerError', 'response': str(e) }
        except docker.errors.ImageNotFound as e:
            return { 'status': 'ImageNotFound', 'response': str(e) }
        except docker.errors.APIError as e:
            return { 'status': 'APIError', 'response': str(e) }

    def create_container(self, image, environment={}, command=None, auto_remove=True, detach=True):
        try:
            container = self.client.create(
                image=image,
                environment=environment,
                command=command,
                auto_remove=auto_remove,
                detach=detach
            )
            # run container.start() to run
            # run container.stop() to stop
            # run container.pause() to pause
            # run container.kill(signal=SIGKILL) to kill
            return { 'status': 200, 'response': container }
        except docker.errors.ImageNotFound as e:
            return { 'status': 'ImageNotFound', 'response': str(e) }
        except docker.errors.APIError as e:
            return { 'status': 'APIError', 'response': str(e) }
