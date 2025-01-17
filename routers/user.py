from fastapi import APIRouter, Depends, HTTPException,status,Request
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from datetime import datetime, timedelta
from db import SessionLocal
from services.user_service import UserService, UserCreate
from models.user import User
from utils.background import log_dependency

# 配置
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


# 获取数据库 session 的依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 工具函数
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_password_hash(password: str):
    return pwd_context.hash(password)


# 从请求头中提取 token


# 获取请求头中的授权信息
def get_authorization_header(request: Request):
    authorization = request.headers.get("Authorization")
    if not authorization:
        return None
    return authorization

def get_token_from_header(authorization: str = Depends(get_authorization_header)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token is missing",
        )
    parts = authorization.split()
    if parts[0].lower() != "bearer" or len(parts) == 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization code",
        )
    return parts[1]


def get_current_user(db: Session = Depends(get_db), token: str = Depends(get_token_from_header)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_service = UserService(db)
    user = user_service.get_user_by_username(username)
    if not user or "message" in user:
        raise credentials_exception
    return user


# 登录接口
@router.post("/login")
async def login(name: str, password: str,log_message:str="", db: Session = Depends(get_db),_:str = Depends(log_dependency)):
    print('777')
    user_service = UserService(db)
    user = user_service.get_user_info(name)
    if not user or "message" in user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user["password"]):  # 使用password字段
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": name}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# 注册用户
@router.post("/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user.password = get_password_hash(user.password)  # 密码加密
    return user_service.create_user(user)


@router.get("/")
async def get_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_all_users()


# 根据用户名获取用户（需要认证）
@router.get("/{name}")
async def get_user_by_username(name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_service = UserService(db)
    user = user_service.get_user_by_username(name)
    if "message" in user:
        raise HTTPException(status_code=404, detail=user["message"])
    return user