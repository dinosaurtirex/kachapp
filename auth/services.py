import uuid 
import datetime as dt
from auth.models import User, Token
from orm.settings import TOKEN_LIFESPAN


async def _validate_register(
    email: str,
    password: str,
    username: str
) -> None:
    if "@" and "." not in email:
        raise ValueError("Incorrect email")
    if len(password) < 6:
        raise ValueError("Not enough big password")
    if await User.get_or_none(username=username) is not None:
        raise ValueError(f"This {username} is already exists")


async def create_user(
    email: str,
    username: str,
    password: str,
    name: str = "",
    surname: str = ""
) -> User:
    await _validate_register(
        email, 
        password,
        username
    )
    return await User.create(
        email = email,
        username = username, 
        password = password,
        name = name,
        surname = surname
    )


async def logout(owner: User) -> None:
    for token in await Token.filter(owner=owner):
        token.expiration_date = dt.date.today()
        await token.save()


async def create_token(owner: User) -> Token:
    token_string = (str(uuid.uuid4()).replace("-","") * 2)[:64]
    return await Token.create(
        owner=owner,
        token=token_string,
        expiration_date=dt.datetime.now() + dt.timedelta(days=TOKEN_LIFESPAN)
    )


async def _validate_user(
    email_or_username: str,
    password: str 
) -> User:
    get_by_email = await User.get_or_none(
        email=email_or_username,
        password=password
    )
    if get_by_email is None: 
        ...
    else:
        return get_by_email
    get_by_username = await User.get_or_none(
        username=email_or_username,
        password=password
    )
    if get_by_username is None:
        raise ValueError("No such user")
    return get_by_username


async def login(
    email_or_username: str,
    password: str,
) -> Token:
    user = await _validate_user(
        email_or_username, password
    )
    return await create_token(user)
