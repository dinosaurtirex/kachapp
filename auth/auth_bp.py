from sanic import Blueprint, Request
from sanic.response import HTTPResponse, json 
from orm.settings import BLUEPRINTS
from orm.settings import API_CODES

from auth.services import (
    create_user,
    login
)


auth_bp = Blueprint(BLUEPRINTS["auth_bp"])


@auth_bp.route("/api/register", methods=["GET"])
async def register_view(request: Request) -> HTTPResponse:
    """
    openapi:
    ---
    operationId: register
    parameters:
      - name: email
        in: query
        required: true
        schema:
          type: string
          format: string
      - name: username
        in: query
        required: true
        schema:
          type: string
          format: string
      - name: password
        in: query
        required: true
        schema:
          type: string
          format: string
      - name: name
        in: query
        required: true
        schema:
          type: string
          format: string
      - name: surname
        in: query
        required: true
        schema:
          type: string
          format: string
    responses:
      '200':
        description: application/json
      '500':
        description: server error
    """
    try:
        new_user = await create_user(
            request.args.get("email"),
            request.args.get("username"),
            request.args.get("password"),
            request.args.get("name"),
            request.args.get("surname")
        )
        return json({
            "status": API_CODES[4000],
            "response": await new_user.serialize()
        })
    except Exception as exc:
        return json({
            "status": API_CODES[4001],
            "error": str(exc)
        })


@auth_bp.route("/api/login", methods=["GET"])
async def login_view(request: Request) -> HTTPResponse:
    """
    openapi:
    ---
    operationId: login
    parameters:
      - name: email_or_username
        in: query
        required: true
        schema:
          type: string
          format: string
      - name: password
        in: query
        required: true
        schema:
          type: string
          format: string
    responses:
      '200':
        description: application/json
      '500':
        description: server error
    """
    try:
        new_token = await login(
            request.args.get("email_or_username"),
            request.args.get("password")
        )
        return json({
            "status": API_CODES[4000],
            "response": await new_token.serialize()
        })
    except Exception as exc:
        return json({
            "status": API_CODES[4001],
            "error": str(exc)
        })
    

@auth_bp.route("/api/check_auth", methods=["GET"])
async def check_auth_view(request: Request) -> HTTPResponse:
    from auth.models import Token 

    token = await Token.get(
        token = request.args.get("token")
    )
    owner = await token.owner 
    return json({
        "status": API_CODES[4000],
        "user": await owner.serialize()
    })