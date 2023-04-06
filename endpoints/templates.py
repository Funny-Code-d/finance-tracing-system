from fastapi import APIRouter, Depends, HTTPException, status
from repository.token import TokenRepository
from models.templates import GetReport, TemplatesIn, GetTemplates, DeleteTemplate, PatchTemplate, GetGeneralStatistics
from repository.templates import TemplatesRepositry
from .depends import get_templates_repositories

route = APIRouter()

@route.post("/", status_code=204)
async def add_templates(
    token: str,
    data: TemplatesIn,
    templates_repositories: TemplatesRepositry = Depends(get_templates_repositories)):
    
    return await templates_repositories.create(
        name_template=data.name_template,
        number_days=data.number_days,
        categoies=data.categories,
        customer_sk=data.customer_sk,
        group_sk=data.group_sk,
        token=token
    )

@route.get("/", status_code=200)
async def get_all(
    token: str,
    customer_sk: int,
    group_sk: str,
    templates_repositories: TemplatesRepositry = Depends(get_templates_repositories)):
    
    return await templates_repositories.get_all(
        customer_sk=customer_sk,
        group_sk=group_sk,
        token=token
    )


@route.delete("/", status_code=200)
async def delete_template(
    token: str,
    data: DeleteTemplate,
    templates_repositories: TemplatesRepositry = Depends(get_templates_repositories)):
    
    return await templates_repositories.delete_template(
        template_sk=data.template_sk,
        customer_sk=data.customer_sk,
        group_sk=data.group_sk,
        token=token
    )

# @route.patch("/", status_code=204)
# async def patch_template(
#     token: str,
#     template_data: PatchTemplate,
#     templates_repositories: TemplatesRepositry = Depends(get_templates_repositories),
#     token_repositories: TokenRepository = Depends(get_token_repositories)):
    
#     return await templates_repositories.patch_template(template_data)

# @route.get("/general", status_code=200)
# async def get_general_statistics(
#     token: str,
#     template_data: GetGeneralStatistics,
#     templates_repositories: TemplatesRepositry = Depends(get_templates_repositories),
#     token_repositories: TokenRepository = Depends(get_token_repositories)):
    
#     return await templates_repositories.get_general_statistics(template_data)

# @route.get("/general/detail", status_code=200)
# async def get_general_statistics_detail(
#     token: str,
#     customer_sk: int,
#     group_sk: str,
#     number_days: int,
#     templates_repositories: TemplatesRepositry = Depends(get_templates_repositories),
#     token_repositories: TokenRepository = Depends(get_token_repositories)):
    
#     return await templates_repositories.get_general_statistics_detail(template_data)


# @route.get("/{template_sk}", status_code=200)
# async def get_general_statistics_detail(
#     token: str,
#     customer_sk: int,
#     group_sk: str,
#     template_sk: int,
#     templates_repositories: TemplatesRepositry = Depends(get_templates_repositories),
#     token_repositories: TokenRepository = Depends(get_token_repositories)):
    
#     return await templates_repositories.get_report(template_data)