from fastapi import APIRouter, Depends, HTTPException, status
from repository.token import TokenRepository
from models.templates import TemplatesIn, GetTemplates, DeleteTemplate, PatchTemplate
from repository.templates import TemplatesRepositry
from .depends import get_templates_repositories, get_token_repositories

route = APIRouter()

@route.post("/", status_code=204)
async def add_templates(
    token: str,
    template_data: TemplatesIn,
    templates_repositories: TemplatesRepositry = Depends(get_templates_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    template_data.token_sk = token_sk
    return await templates_repositories.add_template(template_data)

@route.get("/", status_code=200)
async def get_all(
    token: str,
    customer_sk: int,
    group_sk: str,
    templates_repositories: TemplatesRepositry = Depends(get_templates_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    template_data = GetTemplates(
        token_sk=token_sk,
        customer_sk=customer_sk,
        group_sk=group_sk
    )
    return await templates_repositories.get_all(template_data)


@route.delete("/", status_code=204)
async def delete_template(
    token: str,
    template_data: DeleteTemplate,
    templates_repositories: TemplatesRepositry = Depends(get_templates_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    template_data.token_sk = token_sk
    return await templates_repositories.delete_template(template_data)

@route.patch("/", status_code=204)
async def patch_template(
    token: str,
    template_data: PatchTemplate,
    templates_repositories: TemplatesRepositry = Depends(get_templates_repositories),
    token_repositories: TokenRepository = Depends(get_token_repositories)):
    
    token_sk = await token_repositories.verify_access_token(token)
    template_data.token_sk = token_sk
    return await templates_repositories.patch_template(template_data)