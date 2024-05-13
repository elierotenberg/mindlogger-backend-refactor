import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from apps.workspaces.constants import StorageType
from apps.workspaces.service import workspace
from config import settings
from infrastructure.utility.cdn_arbitrary import ArbitraryAzureCdnClient, ArbitraryGCPCdnClient, ArbitraryS3CdnClient
from infrastructure.utility.cdn_client import CDNClient
from infrastructure.utility.cdn_config import CdnConfig


async def select_storage(
    *,
    applet_id: uuid.UUID | None = None,
    owner_id: uuid.UUID | None = None,
    session: AsyncSession,
):
    service = workspace.WorkspaceService(session, uuid.uuid4())
    if applet_id:
        info = await service.get_arbitrary_info_if_use_arbitrary(applet_id)
    elif owner_id:
        info = await service.get_arbitrary_info_by_owner_id_if_use_arbitrary(owner_id)
    else:
        raise ValueError("Applet id or owner id should be specified.")
    if not info:
        config_cdn = CdnConfig(
            endpoint_url=settings.cdn.endpoint_url,
            region=settings.cdn.region,
            bucket=settings.cdn.bucket_answer,
            ttl_signed_urls=settings.cdn.ttl_signed_urls,
            access_key=settings.cdn.access_key,
            secret_key=settings.cdn.secret_key,
        )
        return CDNClient(config_cdn, env=settings.env)

    bucket_type = info.storage_type.lower()
    arbitrary_cdn_config = CdnConfig(
        region=info.storage_region,
        bucket=info.storage_bucket,
        ttl_signed_urls=settings.cdn.ttl_signed_urls,
        access_key=info.storage_access_key,
        secret_key=info.storage_secret_key,
    )
    match bucket_type:
        case StorageType.AZURE:
            return ArbitraryAzureCdnClient(
                sec_key=info.storage_secret_key,
                bucket=str(info.storage_bucket),
            )
        case StorageType.GCP:
            return ArbitraryGCPCdnClient(
                arbitrary_cdn_config,
                endpoint_url=settings.cdn.gcp_endpoint_url,
                env=settings.env,
            )
        case _:
            # default is aws (logic from legacy app)
            return ArbitraryS3CdnClient(arbitrary_cdn_config, env=settings.env)
