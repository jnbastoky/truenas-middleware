from collections import defaultdict
from itertools import chain, repeat

from .utils import get_docker_client, PROJECT_KEY


def list_resources_by_project(project_name: str | None = None) -> dict[str, dict[str, list]]:
    client = get_docker_client()
    label_filter = {'label': f'{PROJECT_KEY}={project_name}' if project_name else PROJECT_KEY}
    containers = client.containers.list(all=True, filters=label_filter, sparse=False)
    networks = client.networks.list(filters=label_filter)
    volumes = client.volumes.list(filters=label_filter)
    projects = defaultdict(lambda: {'containers': [], 'networks': [], 'volumes': []})

    for resource_type, resource in chain(
        zip(repeat('containers'), containers), zip(repeat('networks'), networks), zip(repeat('volumes'), volumes)
    ):
        projects[
            resource.labels[PROJECT_KEY] if resource_type == 'containers' else resource.attrs['Labels'][PROJECT_KEY]
        ][resource_type].append(resource.attrs)

    return projects
