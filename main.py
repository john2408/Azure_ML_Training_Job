from unicodedata import name
from azureml.core import Workspace, Environment, ScriptRunConfig, Experiment
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
import json



def create_azure_connection(config: dict) -> Workspace:
    subscription_id = config['subscription_id']
    resource_group  = config['resource_group']
    workspace_name  = config['workspace_name']


    try:
        ws = Workspace(subscription_id = subscription_id, 
                        resource_group = resource_group, 
                        workspace_name = workspace_name)

        ws.write_config()
        print('Library configuration succeeded')

        return ws
    except:
        print('Workspace not found')
        return None


def define_environment(env_name : str = "fastai2") -> Environment:
    
    env = Environment(env_name)

    env.docker.base_image = None
    env.docker.base_dockerfile = "./Dockerfile"

    return env

def attach_computing_target(ws: Workspace,
                            cluster_name: str = "gpu-cluster", 
                            ) -> ComputeTarget:

    try:
        compute_target = ComputeTarget(workspace=ws, name=cluster_name)
        print('Found existing compute target.')
    except ComputeTargetException:
        print('Creating a new compute target...')
        compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_NC6',
                                                            max_nodes=4)

        # Create the cluster.
        compute_target = ComputeTarget.create(ws, cluster_name, compute_config)

        compute_target.wait_for_completion(show_output=True)

    # Use get_status() to get a detailed status for the current AmlCompute.
    print(compute_target.get_status().serialize())
        
    return compute_target


def run_training_job(source_directory: str, 
                    ws : Workspace, 
                    env : Environment, 
                    script : str  =' train.py'):

    src = ScriptRunConfig(source_directory = source_directory,
                        script = script,
                        compute_target = compute_target,
                        environment = env)

    run = Experiment(ws,'Tutorial-fastai').submit(src)
    run.wait_for_completion(show_output=True)

if __name__ == '__main__':

    with open('config.json') as f:
        config = json.load(f)
        print(config)


    ws = create_azure_connection(config)

    env = define_environment(env_name = "fastai2")

    compute_target = attach_computing_target(ws,
                            cluster_name = "gpu-cluster", 
                            )

    run_training_job(source_directory = 'fastai-example', 
                    ws = ws, 
                    env = env, 
                    script = 'train.py')
