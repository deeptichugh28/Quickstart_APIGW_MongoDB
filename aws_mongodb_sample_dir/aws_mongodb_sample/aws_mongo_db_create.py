from aws_cdk import (Stack, CfnOutput, Fn)
from constructs import Construct

from awscdk_resources_mongodbatlas import (AdvancedRegionConfig, AdvancedReplicationSpec, DatabaseUserProps, RoleDefinition,
                                           Specs, AccessListDefinition, IpAccessListProps,
                                           ProjectProps, ClusterProps, AtlasBasic,
                                           AdvancedRegionConfigProviderName)
from global_args import GlobalArgs
import os
from dotenv import find_dotenv, load_dotenv

class AwsMongodbAtlasCreateStack(Stack):

  dotenv_path = find_dotenv();
  load_dotenv(dotenv_path);

  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    org_id_var = os.getenv("ORG_ID"),
    region_var =  GlobalArgs.REGION_NAME,
    profile_name_var = GlobalArgs.PROFILE,
    ip_addr_var = GlobalArgs.IP_ADDRESS,
    ip_comment_var = GlobalArgs.IP_COMMENT
    instanceSize = GlobalArgs.INSTANCE_SIZE
    ebsVolumeType = GlobalArgs.EBS_VOLUME_TYPE
    backingProviderName = GlobalArgs.BACKING_PROVIDER_NAME
    username = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASSWORD")

    region_configs_var = [
            AdvancedRegionConfig(analytics_specs=Specs(node_count=1, instance_size=instanceSize, ebs_volume_type=ebsVolumeType),
                                 electable_specs=Specs(node_count=3, instance_size=instanceSize, ebs_volume_type=ebsVolumeType),
                                 priority=7,
                                 provider_name=AdvancedRegionConfigProviderName.TENANT,
                                 backing_provider_name=backingProviderName,
                                 region_name=''.join(region_var))]
    replication_specs_var = [AdvancedReplicationSpec(advanced_region_configs=region_configs_var, num_shards=1)]

    access_list_defs_var = [AccessListDefinition(ip_address=''.join(ip_addr_var), comment=''.join(ip_comment_var))]

    self.atlas_basic_l3 = AtlasBasic(self, "AtlasBasic-py-l3",
                                    cluster_props=ClusterProps(
                                        replication_specs = replication_specs_var
                                    ),
                                    db_user_props=DatabaseUserProps(
                                        database_name=GlobalArgs.AUTH_DATABASE_NAME, 
                                        username=username,
                                        password=password
                                    ),
                                    project_props=ProjectProps(
                                        org_id = ''.join(org_id_var)
                                    ),
                                    ip_access_list_props=IpAccessListProps(
                                        access_list = access_list_defs_var
                                    ),
                                    profile=''.join(profile_name_var)
                                )
    
    serveraddress = self.atlas_basic_l3.m_cluster.connection_strings.standard_srv
    
    CfnOutput(self,
                  f"serveradd",
                  description=f"Server Address",
                  value=self.atlas_basic_l3.m_cluster.connection_strings.standard_srv)
    
    self.clusteraddress = Fn.select(2, Fn.split('/', serveraddress))
                  
    self.Atlas_URI = f"mongodb+srv://" + username + ":" + password + "@" + self.clusteraddress
        
    # properties to share with other stacks
    @property
    def get_connection_string_srv(self):
        return self.Atlas_URI

    


