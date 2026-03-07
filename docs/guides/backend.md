# 后端开发指南

## 1. 角色职责

作为后端开发，你负责:
- API 开发
- 数据库设计
- 业务逻辑实现
- 性能优化
- 后端部署

## 2. 技术栈

### 2.1 Python 服务

- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **数据库**: PostgreSQL
- **缓存**: Redis
- **认证**: JWT

### 2.2 Go 服务

- **框架**: Gin
- **ORM**: GORM
- **数据库**: PostgreSQL
- **缓存**: Redis
- **RPC**: gRPC

## 3. 工作流程

### 3.1 开发环境

**Python**:
```bash
cd backend/python
python main.py
```

**Go**:
```bash
cd backend/go
go run main.go
```

### 3.2 API 开发

**Python (FastAPI)**:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/users")
def get_users(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    users = db.query(User).limit(limit).offset(offset).all()
    return {"code": 0, "data": users}

@router.post("/users")
def create_user(user: CreateUserDto, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    return {"code": 0, "data": db_user}
```

**Go (Gin)**:
```go
func GetUsers(c *gin.Context) {
    var users []User
    db.Find(&users)
    c.JSON(http.StatusOK, gin.H{
        "code": 0,
        "data": users,
    })
}

func CreateUser(c *gin.Context) {
    var user User
    if err := c.ShouldBindJSON(&user); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    db.Create(&user)
    c.JSON(http.StatusOK, gin.H{
        "code": 0,
        "data": user,
    })
}
```

### 3.3 数据库设计

**Python (SQLAlchemy)**:
```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Go (GORM)**:
```go
type User struct {
    ID        uint      `gorm:"primaryKey"`
    Name      string    `gorm:"size:100;not null"`
    Email     string    `gorm:"size:100;uniqueIndex;not null"`
    CreatedAt time.Time
}
```

## 4. Skills

### 4.1 api-design

API 设计与实现。

**使用**:
```bash
amazing skill run api-design --resource user
```

### 4.2 database-design

数据库设计。

**使用**:
```bash
amazing skill run database-design --entity user
```

### 4.3 auth-implement

认证授权实现。

**使用**:
```bash
amazing skill run auth-implement --method jwt
```

## 5. 认证授权

### 5.1 JWT 认证

**Python**:
```python
from jose import jwt
from datetime import datetime, timedelta

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=1440)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None
```

**Go**:
```go
import "github.com/golang-jwt/jwt/v5"

func CreateToken(userID uint) (string, error) {
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
        "user_id": userID,
        "exp":     time.Now().Add(time.Hour * 24).Unix(),
    })
    return token.SignedString([]byte(SECRET_KEY))
}

func VerifyToken(tokenString string) (*jwt.Token, error) {
    return jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
        return []byte(SECRET_KEY), nil
    })
}
```

### 5.2 权限控制

```python
from fastapi import Depends, HTTPException

def require_permission(permission: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user.has_permission(permission):
                raise HTTPException(status_code=403, detail="Permission denied")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@router.post("/users")
@require_permission("user:create")
def create_user(user: CreateUserDto):
    pass
```

## 6. 测试

### 6.1 单元测试

**Python (Pytest)**:
```python
def test_create_user(client):
    response = client.post("/api/v1/users", json={
        "name": "张三",
        "email": "test@example.com"
    })
    assert response.status_code == 200
    assert response.json()["code"] == 0
```

**Go**:
```go
func TestCreateUser(t *testing.T) {
    router := setupRouter()
    w := httptest.NewRecorder()
    body := `{"name":"张三","email":"test@example.com"}`
    req, _ := http.NewRequest("POST", "/api/v1/users", strings.NewReader(body))
    router.ServeHTTP(w, req)
    assert.Equal(t, 200, w.Code)
}
```

### 6.2 运行测试

**Python**:
```bash
pytest
```

**Go**:
```bash
go test ./...
```

## 7. 数据库迁移

### 7.1 Alembic (Python)

```bash
# 创建迁移
alembic revision --autogenerate -m "create users table"

# 执行迁移
alembic upgrade head

# 回滚
alembic downgrade -1
```

### 7.2 GORM AutoMigrate (Go)

```go
db.AutoMigrate(&User{}, &Role{})
```

## 8. 权限

作为后端开发，你拥有以下权限:
- `api:develop` - API 开发
- `database:design` - 数据库设计
- `service:create` - 服务创建
- `backend:deploy` - 后端部署

## 9. 最佳实践

### 9.1 错误处理

**Python**:
```python
from fastapi import HTTPException

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"code": 0, "data": user}
```

**Go**:
```go
func GetUser(c *gin.Context) {
    id := c.Param("id")
    var user User
    if err := db.First(&user, id).Error; err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
        return
    }
    c.JSON(http.StatusOK, gin.H{"code": 0, "data": user})
}
```

### 9.2 日志记录

**Python**:
```python
import logging

logger = logging.getLogger(__name__)

@router.post("/users")
def create_user(user: CreateUserDto):
    logger.info(f"Creating user: {user.name}")
    # ...
    logger.info(f"User created: {db_user.id}")
```

**Go**:
```go
import "log"

func CreateUser(c *gin.Context) {
    log.Printf("Creating user")
    // ...
    log.Printf("User created: %d", user.ID)
}
```

### 9.3 性能优化

- 使用索引
- 查询优化
- 使用缓存
- 连接池配置
- 异步处理
